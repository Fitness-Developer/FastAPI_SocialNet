from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate

def create_post(db: Session, post: PostCreate, user_id: int):
    db_post = Post(**post.dict(),author_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts(db: Session, skip=0, limit=10):
    return db.query(Post).offset(skip).limit(limit).all()

def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def update_post(db: Session, post_id: int, post: PostUpdate):
    db_post = get_post(db, post_id)
    if db_post:
        for key, value in post.dict().items():
            setattr(db_post, key, value)
        db.commit()
        db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int):
    db_post = get_post(db,post_id)
    if db_post:
        db.delete(db_post)
        db.commit()
