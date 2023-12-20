from sqlalchemy.orm import Session
from ..db.models.message import Message as MessageModel
from ..schemas.message_schema import MessageCreate, MessageUpdate

def create_message(db: Session, message: MessageCreate):
    db_message = MessageModel(UserId=message.UserId, ReceiverId=message.ReceiverId, Message=message.Message)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_message(db: Session, message_id: int):
    return db.query(MessageModel).filter(MessageModel.Id == message_id).first()

def get_direct_messages(db: Session, user_id: int, receiver_id: int, skip: int = 0, limit: int = 10):
    query = db.query(MessageModel).filter(
        (MessageModel.UserId == user_id) & (MessageModel.ReceiverId == receiver_id)
    ).order_by(MessageModel.Id).offset(skip).limit(limit).all()
    return query

def get_broadcast_messages(db: Session, skip: int = 0, limit: int = 10):
    # Retrieve broadcast messages (ReceiverId is 1) with pagination
    broadcast_messages = (
        db.query(MessageModel)
        .filter(MessageModel.ReceiverId == 1)
        .order_by(MessageModel.Id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return broadcast_messages


def get_messages(db: Session, skip: int = 0, limit: int = 10):
    return db.query(MessageModel).order_by(MessageModel.Id).offset(skip).limit(limit).all()

def update_message(db: Session, message_id: int, message: MessageUpdate):
    db_message = get_message(db, message_id)
    if db_message:
        for key, value in message.dict(exclude_unset=True).items():
            setattr(db_message, key, value)
        db.commit()
        db.refresh(db_message)
    return db_message

def delete_message(db: Session, message_id: int):
    db_message = get_message(db, message_id)
    if db_message:
        db.delete(db_message)
        db.commit()
    return db_message
