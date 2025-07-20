from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer,primary_key=True)
    content = Column(Text)
    created_at = Column(DateTime,default=datetime.utcnow)

    author_id = Column(Integer,ForeignKey("users.id"))
    post_id = Column(Integer,ForeignKey("posts.id"))

    author = relationship("User",back_populates="comments")
    post = relationship("Post",back_populates="comments")
