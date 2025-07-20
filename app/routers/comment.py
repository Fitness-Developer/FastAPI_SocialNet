from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.comment import CommentCreate, CommentOut
from app.crud import comment as crud_comment
from app.dependencies import get_db, get_current_user
from app.cache.redis_client import get_cache, set_cache, redis_client


router = APIRouter(prefix="/comments",tags=["Comments"])

@router.post("/", response_model=CommentOut)
def create_comment(commnet: CommentCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    return crud_comment.create_comment(db,commnet,user.id)

@router.get("/post/{post_id}",response_model=List[CommentOut])
def get_comment(post_id: int, db: Session = Depends(get_db)):
    cache_key = f"comments:post:{post_id}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    comments = crud_comment.get_comments_by_post(db,post_id)
    result = [CommentOut.model_validate(comment).model_dump(mode="json") for comment in comments]
    set_cache(cache_key, result, expire=30)
    return result

@router.delete("/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    comment = crud_comment.get_comment(db, comment_id)
    if not comment or comment.author_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this comment")
    crud_comment.delete_comment(db, comment_id)

    redis_client.delete(f"comments:post:{comment_id}")
    return {"detail": "Deleted"}