import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.models_dao import ProjectDAO, SkillDAO, WorkExperienceDAO, EducationDAO, BlogPostDAO, TestimonialDAO, SocialMediaDAO, ProfileDAO, ProjectTagDAO, MessageDAO, MLPredictionDAO
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from app.config import settings
import logging

logger = logging.getLogger(__name__)

async def load_knowledge_base(db: AsyncSession):
    projects = await ProjectDAO.get_all(db)
    skills = await SkillDAO.get_all(db)
    work_experiences = await WorkExperienceDAO.get_all(db)
    educations = await EducationDAO.get_all(db)
    blogposts = await BlogPostDAO.get_all(db)
    testimonials = await TestimonialDAO.get_all(db)
    social_medias = await SocialMediaDAO.get_all(db)
    profiles = await ProfileDAO.get_all(db)
    project_tags = await ProjectTagDAO.get_all(db)

    documents = []

    for project in projects:
        tags = [tag.tag_name for tag in project_tags if tag.project_id == project.id]
        documents.append(Document(page_content=(
            f"Project: {project.title}\n"
            f"Description: {project.description or 'No description'}\n"
            f"URL: {project.project_url or 'No URL'}\n"
            f"Completed: {project.date_completed or 'Not completed'}\n"
            f"Tags: {', '.join(tags) if tags else 'No tags'}"
        )))

    for skill in skills:
        documents.append(Document(page_content=(
            f"Skill: {skill.skill_name}\n"
            f"Description: {skill.description or 'No description'}\n"
            f"Proficiency: {skill.proficiency_level or 'Not specified'}"
        )))

    for experience in work_experiences:
        documents.append(Document(page_content=(
            f"Work Experience: {experience.position} at {experience.company}\n"
            f"Description: {experience.description or 'No description'}\n"
            f"Period: {experience.start_date} to {experience.end_date or 'Present'}"
        )))

    for education in educations:
        documents.append(Document(page_content=(
            f"Education: {education.degree or 'No degree'} in {education.field_of_study or 'No field'}\n"
            f"Institution: {education.institution or 'No institution'}\n"
            f"Period: {education.start_date} to {education.end_date or 'Present'}"
        )))

    for blogpost in blogposts:
        documents.append(Document(page_content=(
            f"Blog Post: {blogpost.title}\n"
            f"Content: {blogpost.content or 'No content'}\n"
            f"Published: {blogpost.published_date or 'Not published'}"
        )))

    for testimonial in testimonials:
        documents.append(Document(page_content=(
            f"Testimonial: {testimonial.quote}\n"
            f"Author: {testimonial.author}\n"
            f"Date: {testimonial.date or 'No date'}"
        )))

    for social in social_medias:
        documents.append(Document(page_content=(
            f"Social Media: {social.platform_name}\n"
            f"Profile URL: {social.profile_url}"
        )))

    for profile in profiles:
        documents.append(Document(page_content=(
            f"Profile: {profile.name}\n"
            f"Bio: {profile.bio or 'No bio'}\n"
            f"Email: {profile.email or 'No email'}\n"
            f"Phone: {profile.phone or 'No phone'}\n"
            f"Address: {profile.address or 'No address'}\n"
            f"Resume URL: {profile.resume_url or 'No resume'}"
        )))

    return documents

async def get_rag_response(question: str, db: AsyncSession) -> str:
    try:
        documents = await load_knowledge_base(db)
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=settings.GEMINI_API_KEY)
        vector_store = FAISS.from_documents(documents, embeddings)
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=settings.GEMINI_API_KEY)

        prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="You are Ilya Koryaev's assistant for his portfolio. Answer the question based on the provided context in a friendly and professional tone.\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:"
        )
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever(),
            chain_type_kwargs={"prompt": prompt_template}
        )

        response = qa_chain.run(question)
        await MessageDAO.create(db, {
            "name": "RAG User",
            "email": "bot@portfolio.com",
            "message": question,
            "source": "rag",
            "created_at": datetime.utcnow()
        })
        await MLPredictionDAO.create(db, {
            "input_text": question,
            "prediction": response,
            "created_at": datetime.utcnow()
        })
        return response
    except Exception as e:
        logger.error(f"Unexpected error processing RAG query: {str(e)}")
        return "Произошла ошибка при обработке вопроса. Попробуйте позже."