from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.message import Message as MessageModel
from app.schemas.message import Message, MessageCreate, MessageUpdate

router = APIRouter()


@router.get("/", response_model=List[Message])
def get_messages(
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(MessageModel)
    if category:
        query = query.filter(MessageModel.category == category)
    return query.offset(skip).limit(limit).all()


@router.post("/", response_model=Message)
def create_message(
    message: MessageCreate,
    db: Session = Depends(get_db)
):
    db_message = MessageModel(**message.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


@router.get("/{message_id}", response_model=Message)
def get_message(
    message_id: int,
    db: Session = Depends(get_db)
):
    message = db.query(MessageModel).filter(MessageModel.id == message_id).first()
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return message


@router.patch("/{message_id}", response_model=Message)
def update_message(
    message_id: int,
    message: MessageUpdate,
    db: Session = Depends(get_db)
):
    db_message = db.query(MessageModel).filter(MessageModel.id == message_id).first()
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    
    update_data = message.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_message, field, value)
    
    db.commit()
    db.refresh(db_message)
    return db_message


@router.delete("/{message_id}")
def delete_message(
    message_id: int,
    db: Session = Depends(get_db)
):
    message = db.query(MessageModel).filter(MessageModel.id == message_id).first()
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    
    db.delete(message)
    db.commit()
    return {"ok": True}


@router.get("/unprocessed/", response_model=List[Message])
def get_unprocessed_messages(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """获取所有未处理的消息"""
    messages = db.query(MessageModel)\
        .filter(MessageModel.processed == False)\
        .order_by(MessageModel.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    return messages


@router.put("/process/{message_id}", response_model=Message)
def process_message(
    message_id: int,
    db: Session = Depends(get_db)
):
    """将消息标记为已处理"""
    message = db.query(MessageModel).filter(MessageModel.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.processed = True
    db.commit()
    db.refresh(message)
    return message
