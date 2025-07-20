from sqlalchemy.orm import Session
from app.models.message import Message

def create_message(db: Session, sender_id: int, receiver_id: int, content: str):
    msg = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_history(db: Session, user_id: int, current_user_id: int):
    return db.query(Message).filter(
        ((Message.sender_id == current_user_id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user_id))
    ).all()

def get_contacts(db: Session, current_user_id: int):
    messages = db.query(Message).filter(
        (Message.sender_id == current_user_id) | (Message.receiver_id == current_user_id)
    ).all()

    contacts = set()
    for m in messages:
        if m.sender_id != current_user_id:
            contacts.add(m.sender_id)
        if m.receiver_id != current_user_id:
            contacts.add(m.receiver_id)
    return list(contacts)

def count_unread(db: Session,from_user_id: int,current_user_id: int):
    count = db.query(Message).filter_by(
        sender_id=from_user_id,
        receiver_id=current_user_id,
        is_read=False
    ).count()
    return count

def delete_message(db: Session, message_id: int):
    message = db.query(Message).filter_by(id=message_id).first()
    db.delete(message)
    db.commit()