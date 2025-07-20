from pydantic import BaseModel
from datetime import datetime

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    post_id: int

class CommentOut(CommentBase):
    id: int
    author_id: int
    post_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }