import datetime
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.models_dao import ProjectDAO, SkillDAO, WorkExperienceDAO, EducationDAO, BlogPostDAO, TestimonialDAO, SocialMediaDAO, ProfileDAO, ProjectTagDAO, MessageDAO, MLPredictionDAO
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from google import genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config import settings
import logging
import re
from typing import List
from app.database import get_db

logger = logging.getLogger(__name__)

def escape_markdown_v2(text: str) -> str:
    """Экранирует специальные символы для MarkdownV2 в Telegram."""
    reserved_chars = r'([_\*[\]()~`>#\+-=|{}\.!])'
    text = re.sub(reserved_chars, r'\\\g<1>', text)
    text = re.sub(r'([\\]{2,})', r'\\', text)
    text = text.replace('\n', '\n\n')
    return text[:1500]  # Увеличили лимит до 1500 символов

async def load_knowledge_base(db: AsyncSession) -> List[Document]:
    logger.debug("Loading knowledge base...")
    try:
        projects = await ProjectDAO.get_all(db)
        skills = await SkillDAO.get_all(db)
        work_experiences = await WorkExperienceDAO.get_all(db)
        educations = await EducationDAO.get_all(db)
        blogposts = await BlogPostDAO.get_all(db)
        testimonials = await TestimonialDAO.get_all(db)
        social_medias = await SocialMediaDAO.get_all(db)
        profiles = await ProfileDAO.get_all(db)
        project_tags = await ProjectTagDAO.get_all_with_tags(db)

        logger.debug(f"Loaded {len(projects)} projects, {len(skills)} skills, {len(work_experiences)} experiences")

        documents = []
        for project in projects:
            tags = [tag.tag_name for tag in project_tags if tag.project_id == project.id]
            documents.append(Document(page_content=(
                f"Project: {project.title}\n"
                f"Description: {project.description.encode('utf-8', errors='replace').decode('utf-8') or 'No description'}\n"
                f"URL: {project.project_url or 'No URL'}\n"
                f"Completed: {project.date_completed or 'Not completed'}\n"
                f"Tags: {', '.join(tags) if tags else 'No tags'}"
            )))

        for skill in skills:
            documents.append(Document(page_content=(
                f"Skill: {skill.skill_name}\n"
                f"Description: {skill.description.encode('utf-8', errors='replace').decode('utf-8') or 'No description'}\n"
                f"Proficiency: {skill.proficiency_level or 'Not specified'}"
            )))

        for experience in work_experiences:
            documents.append(Document(page_content=(
                f"Work Experience: {experience.position} at {experience.company}\n"
                f"Description: {experience.description.encode('utf-8', errors='replace').decode('utf-8') or 'No description'}\n"
                f"Period: {experience.start_date} to {experience.end_date or 'Present'}"
            )))

        for education in educations:
            documents.append(Document(page_content=(
                f"Education: {education.degree or 'No degree'} in {education.field_of_study or 'Not specified'}\n"
                f"Institution: {education.institution or 'Not specified'}\n"
                f"Period: {education.start_date} to {education.end_date or 'Present'}"
            )))

        for blogpost in blogposts:
            documents.append(Document(page_content=(
                f"Blog Post: {blogpost.title}\n"
                f"Content: {blogpost.content.encode('utf-8', errors='replace').decode('utf-8') or 'No content'}\n"
                f"Date: {blogpost.publication_date or 'Not specified'}"
            )))

        for testimonial in testimonials:
            documents.append(Document(page_content=(
                f"Testimonial: From {testimonial.author or 'Anonymous'}\n"
                f"Content: {testimonial.content.encode('utf-8', errors='replace').decode('utf-8') or 'No content'}\n"
                f"Date: {testimonial.date_received or 'Not specified'}"
            )))

        for social_media in social_medias:
            documents.append(Document(page_content=(
                f"Social Media: {social_media.platform}\n"
                f"URL: {social_media.url or 'No URL'}\n"
                f"Username: {social_media.username or 'Not specified'}"
            )))

        for profile in profiles:
            documents.append(Document(page_content=(
                f"Profile: {profile.full_name or 'Not specified'}\n"
                f"Bio: {profile.bio.encode('utf-8', errors='replace').decode('utf-8') or 'No bio'}\n"
                f"Location: {profile.location or 'Not specified'}"
            )))

        logger.debug(f"Generated {len(documents)} documents for knowledge base")
        return documents

    except Exception as e:
        logger.error(f"Error loading knowledge base: {str(e)}")
        return []

async def get_rag_response(question: str, db: AsyncSession) -> str:
    """Получает ответ через RAG с использованием Gemini."""
    logger.debug(f"Processing RAG query: {question.encode('utf-8', errors='replace').decode('utf-8')}")
    try:
        if not settings.GEMINI_API_KEY:
            logger.error("GEMINI_API_KEY is not set in settings")
            raise ValueError("GEMINI_API_KEY is missing")

        documents = await load_knowledge_base(db)
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=settings.GEMINI_API_KEY
        )
        logger.debug("Creating vector store...")
        vector_store = FAISS.from_documents(documents, embeddings)
        logger.debug("Initializing LLM...")
        client = genai.Client(api_key=settings.GEMINI_API_KEY)

        logger.debug("Retrieving relevant documents...")
        retriever = vector_store.as_retriever(search_kwargs={"k": 10})
        relevant_docs = retriever.get_relevant_documents(question)
        context = "\n\n".join([doc.page_content.encode('utf-8', errors='replace').decode('utf-8') for doc in relevant_docs])

        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="Ты ассистент для портфолио IT-специалиста. Отвечай профессионально, но доступно, без сленга. Максимум 1500 символов. Используй эмодзи (🔥🚀💻) для акцента. Контекст: {context}\n\nВопрос: {question}\n\nОтвет:"
        ).format(context=context, question=question)

        logger.debug("Generating response with Gemini...")
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                generation_config={"max_output_tokens": 1500}
            )
        )
        answer = response.text.strip()
        answer = answer.encode('utf-8', errors='replace').decode('utf-8')
        logger.debug(f"Raw Gemini response: {answer[:100]}...")

        if not answer:
            logger.warning("Gemini response is empty")
            return escape_markdown_v2("К сожалению, не удалось сгенерировать ответ. Попробуйте позже! 🚀")

        logger.debug("Saving message and prediction...")
        async for db in get_db():
            message = await MessageDAO.create(db, {
                "name": "RAG User",
                "email": "bot@portfolio.com",
                "message": question,
                "source": "rag",
                "date_sent": datetime.datetime.utcnow()
            })
            await MLPredictionDAO.create(db, {
                "message_id": message.id,
                "input_text": question,
                "prediction": answer,
                "created_at": datetime.datetime.utcnow()
            })
            break

        logger.info(f"RAG response generated: {answer[:100]}...")
        return escape_markdown_v2(answer)

    except Exception as e:
        logger.error(f"Unexpected error processing RAG query: {str(e)}")
        return escape_markdown_v2("К сожалению, произошла ошибка. Попробуйте позже! 🚀")