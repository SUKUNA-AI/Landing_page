from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    role: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
    email: str | None = None
    role: str | None = None

    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: int
    password_hash: str

    class Config:
        from_attributes = True