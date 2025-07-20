from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.schemas.comment import CommentCreate


def create_comment(db: Session, comment: CommentCreate, user_id: int):
    db_comment = Comment(**comment.dict(),author_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments_by_post(db: Session, post_id: int):
    return db.query(Comment).filter(Comment.post_id == post_id).all()

def get_comment(db: Session, comment_id: int):
    return db.query(Comment).filter(Comment.id == comment_id).first()

def delete_comment(db: Session,comment_id: int):
    comment = get_comment(db, comment_id)
    if comment:
        db.delete(comment)
        db.commit()
