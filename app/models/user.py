from sqlalchemy import Column, Integer, String, Enum
from app.database import Base
import enum

class TierEnum(str, enum.Enum):
    free = "free"
    premium = "premium"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    tier = Column(Enum(TierEnum), default=TierEnum.free, nullable=False)
