from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.post import PostOut, PostCreate, PostUpdate
from app.crud import post as crud_post
from app.dependencies import get_db, get_current_user
from app.cache.redis_client import get_cache, set_cache, redis_client


router = APIRouter(prefix="/posts",tags=["Posts"])

@router.post("/", response_model=PostOut)
def create(post: PostCreate,db: Session = Depends(get_db), user=Depends(get_current_user)):
    return crud_post.create_post(db, post, user.id)

@router.get("/", response_model=List[PostOut])
def read_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    cache_key = f"posts:skip={skip}&limit={limit}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    posts = crud_post.get_posts(db,skip,limit)
    result = [PostOut.model_validate(post).model_dump(mode="json") for post in posts]
    set_cache(cache_key,result,expire=30)
    return result


@router.get("/{post_id}",response_model=PostOut)
def read_one(post_id:int,db: Session = Depends(get_db)):
    cache_key = f"post:{post_id}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    post = crud_post.get_post(db,post_id)
    if not post:
        raise HTTPException(status_code=404,detail="Not found")

    result = PostOut.model_validate(post).model_dump(mode="json")
    set_cache(cache_key,result,expire=60)

@router.put("/{post_id}",response_model=PostOut)
def update(post_id: int, updated: PostUpdate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    post = crud_post.get_post(db,post_id)
    if not post or post.author_id != user.id:
        raise HTTPException(status_code=403,detail="Forbidden")
    updated_post = crud_post.update_post(db,post_id,updated)

    set_cache(f"post:{post_id}",PostOut.model_validate(updated_post).model_dump(mode="json"),expire=60)
    return updated_post


@router.delete("/{post_id}")
def delete( post_id: int, db:Session=Depends(get_db),user = Depends(get_current_user)):
    post = crud_post.get_post(db,post_id)
    if not post or post.author_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    crud_post.delete_post(db,post_id)

    redis_client.delete(f"post:{post_id}")
    return {"delete":"Deleted"}

