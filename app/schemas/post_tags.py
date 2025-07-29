from pydantic import BaseModel

class PostTagCreate(BaseModel):
    post_id: int
    tag_id: int

class PostTagResponse(BaseModel):
    post_id: int
    tag_id: int

    class Config:
        from_attributes = True