from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class MessageBase(BaseModel):
    title: str = Field(..., min_length=1, description="Message title")
    content: str = Field(..., min_length=1, description="Message content")
    category: str = Field(..., min_length=1, description="Message category")

    class Config:
        from_attributes = True


class MessageCreate(MessageBase):
    is_read: bool = Field(default=False)
    processed: bool = Field(default=False)


class MessageUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    content: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = Field(None, min_length=1)
    is_read: Optional[bool] = Field(default=None)
    processed: Optional[bool] = Field(default=None)

    class Config:
        from_attributes = True


class Message(MessageBase):
    id: int
    is_read: bool = Field(default=False)
    processed: bool = Field(default=False)
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
