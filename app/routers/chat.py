from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List
from app.schemas.message import MessageOut, MessageCreate
from app.models.message import Message
from app.crud import chat as crud_chat
from app.models.user import User
from app.dependencies import get_db, get_current_user
from app.websockets.connection_manager import ConnectionManager
from app.cache.redis_client import get_cache, set_cache, redis_client

router = APIRouter(prefix="/chat", tags=["Chat"])


# Отправка сообщений
@router.post("/", response_model=MessageOut)
def send_message(msg: MessageCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_chat.create_message(db, current_user.id, msg.receiver_id, msg.content)


# История между 2 пользователями
@router.get("/history/{user_id}", response_model=List[MessageOut])
def get_chat_history(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cache_key = f"history:user:{user_id}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    messages = crud_chat.get_history(db, user_id, current_user.id)
    result = [MessageOut.model_validate(message).model_dump(mode="json") for message in messages]
    set_cache(cache_key, result, expire=30)
    return result


# Список собеседников
@router.get("/contacts", response_model=List[int])
def get_contacts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cache_key = "contacts"
    cached = get_cache(cache_key)
    if cached:
        return cached
    contact_ids = crud_chat.get_contacts(db, current_user.id)
    set_cache(cache_key, contact_ids, expire=30)
    return contact_ids


@router.get("/unread-count/{from_user_id}", response_model=int)
def count_unread(from_user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_chat.count_unread(db, from_user_id, current_user.id)


@router.delete("/{message_id}")
def delete_message(message_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        message = crud_chat.delete_message(db, message_id)
        if not message:
            raise HTTPException(status_code=404, detail="Massege not found")

        redis_client.delete(f"history:user:{current_user.id}")
        redis_client.delete(f"history:user:{message.receiver_id}")
        return {"detail": "Message deleted"}

    except PermissionError:
        raise HTTPException(status_code=403, detail="You can delete only your own messages")

# manager = ConnectionManager()

# @router.websocket("/ws/{user_id}")
# async def websocket_endpoint(websocket: WebSocket, user_id: int):
#     await manager.connect(user_id, websocket)
#     try:
#         while True:
#             data = await websocket.receive_json()
#
#             receiver_id = data["reveiver_id"]
#             content = data["content"]
#
#             db: Session = next(get_db())
#             new_msg = Message(sender_id = user_id, receiver_id=receiver_id, content=content)
#             db.add(new_msg)
#             db.commit()
#             db.refresh(new_msg)
#
#             await manager.send_personal_message(f"{user_id}:{content}",receiver_id)
#
#     except WebSocketDisconnect:
#         manager.disconnect(user_id)
