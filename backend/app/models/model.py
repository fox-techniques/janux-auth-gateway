from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    message = Column(Text, nullable=False)
