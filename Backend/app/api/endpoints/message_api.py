# messages_api.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.message_crud import (
    create_message,
    get_message,
    get_direct_messages,
    get_broadcast_messages,
    get_messages,
    update_message,
    delete_message,
)
from app.schemas.message_schema import MessageCreate, MessageUpdate,Message

from app.db.database import SessionLocal


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/messages/add", response_model=Message)
def create_new_message_endpoint(message: MessageCreate, db: Session = Depends(get_db)):
    return create_message(db, message)

@router.get("/messages/getbyid/{message_id}", response_model=Message)
def read_message_endpoint(message_id: int, db: Session = Depends(get_db)):
    message = get_message(db, message_id)
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

@router.get("/messages/getbyusers/{user_id}/{receiver_id}")
def read_direct_messages_endpoint(
    user_id: int, receiver_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return get_direct_messages(db, user_id, receiver_id, skip, limit)

@router.get("/messages/getbroadcastmessages")
def read_broadcast_messages_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_broadcast_messages(db, skip, limit)

@router.get("/messages/getall")
def read_all_messages_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_messages(db, skip, limit)

@router.put("/messages/update/{message_id}", response_model=Message)
def update_existing_message_endpoint(
    message_id: int, message: MessageUpdate, db: Session = Depends(get_db)
):
    updated_message = update_message(db, message_id, message)
    if updated_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return updated_message

@router.delete("/messages/delete/{message_id}", response_model=Message)
def delete_existing_message_endpoint(message_id: int, db: Session = Depends(get_db)):
    deleted_message = delete_message(db, message_id)
    if deleted_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return deleted_message