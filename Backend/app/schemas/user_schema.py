from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    username: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    name: str | None = None
    username: str | None = None
