from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from app.database import Base
import enum

class ThumbEnum(enum.Enum):
    up = "up"
    down = "down"

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    cityname = Column(String, nullable=False)
    country = Column(String, nullable=False)
    rate = Column(Integer, nullable=False)
    reason = Column(String, nullable=False)
    thumb = Column(Enum(ThumbEnum), nullable=True) 