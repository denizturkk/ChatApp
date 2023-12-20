from sqlalchemy.orm import Session
from ..db.models.user import User as UserModel
from ..schemas.user_schema import UserCreate, UserUpdate

def get_user_by_id(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id== user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(UserModel).order_by(UserModel.id).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    db_user = UserModel(name=user.name, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = get_user_by_id(db, user_id)
    if db_user:
        if user.name is not None:
            db_user.name = user.name
        if user.username is not None:
            db_user.username = user.username
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
