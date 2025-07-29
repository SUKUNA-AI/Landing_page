from pydantic import BaseModel

class SocialMediaCreate(BaseModel):
    user_id: int
    platform_name: str
    profile_url: str

class SocialMediaResponse(BaseModel):
    id: int
    user_id: int
    platform_name: str
    profile_url: str

    class Config:
        from_attributes = True