from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.dependencies import get_db,get_current_user
from app.models.user import User
from app.schemas.user import UserOut

router = APIRouter(prefix="/users",tags=["users"])

@router.get("/",response_model=List[UserOut])
def get_users(query: Optional[str]=None, db:Session = Depends(get_db)):
    users = db.query(User)
    if query:
        users = users.filter(
            (User.username.ilike(f"%{query}%")) |
            (User.email.ilike(f"%{query}%"))
        )
    return users.all()

@router.get("/{user_id}",response_model=UserOut)
def get_user_profile(user_id: int,db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/me",response_model=UserOut)
def update_profile(new_data: UserOut, db: Session = Depends(get_db),current_user:User = Depends(get_current_user)):
    user = db.query(User).get(current_user.id)
    user.username = new_data.username
    user.email = new_data.email
    db.commit()
    db.refresh(user)
    return user
