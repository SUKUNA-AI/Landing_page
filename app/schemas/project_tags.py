from pydantic import BaseModel

class ProjectTagCreate(BaseModel):
    project_id: int
    tag_id: int

class ProjectTagResponse(BaseModel):
    project_id: int
    tag_id: int

    class Config:
        from_attributes = True