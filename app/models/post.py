from sqlalchemy import Column, String, Integer,Text,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer,primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    created_at = Column(DateTime,default=datetime.utcnow)
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User",back_populates="posts")
    comments = relationship("Comment", back_populates="post",cascade="all, delete")
