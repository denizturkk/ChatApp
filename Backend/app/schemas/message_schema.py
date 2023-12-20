from pydantic import BaseModel

class MessageBase(BaseModel):
    UserId: int
    ReceiverId: int
    Message: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    Id: int

    class Config:
        orm_mode = True

class MessageUpdate(BaseModel):
    UserId: int | None = None
    ReceiverId: int | None = None
    Message: str | None = None
