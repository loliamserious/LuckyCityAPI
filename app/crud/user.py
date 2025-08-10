from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas import user as schemas
from typing import Optional
from sqlalchemy.exc import IntegrityError
from app.security.password import get_password_hash, verify_password

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        tier=user.tier
    )
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise
    return user

def reset_password(db: Session, email: str, new_password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if user:
        user.hashed_password = get_password_hash(new_password)
        db.commit()
        db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
