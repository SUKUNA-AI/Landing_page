from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password_hash: str
    email: str
    role: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True