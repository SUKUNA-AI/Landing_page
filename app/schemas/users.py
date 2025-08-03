from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password_hash: str
    email: str
    role: str

class UserUpdate(BaseModel):
    username: str | None = None
    password_hash: str | None = None
    email: str | None = None
    role: str | None = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True