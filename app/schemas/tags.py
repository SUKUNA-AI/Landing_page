from pydantic import BaseModel

class TagCreate(BaseModel):
    tag_name: str

class TagResponse(BaseModel):
    id: int
    tag_name: str

    class Config:
        from_attributes = True