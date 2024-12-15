from sqlalchemy import Column, Integer, String, DateTime, Boolean, CheckConstraint, func, text
from datetime import datetime
import pytz
from app.db.session import Base
from app.core.config import settings


def now_with_timezone():
    return datetime.now(pytz.timezone(settings.TIMEZONE))


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)
    category = Column(String, index=True, nullable=False)
    is_read = Column(Boolean, default=False)
    processed = Column(Boolean, default=False, index=True)  # 新增字段，用于标记消息是否已处理
    created_at = Column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        default=now_with_timezone
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=now_with_timezone
    )

    __table_args__ = (
        CheckConstraint("length(title) > 0", name="title_not_empty"),
        CheckConstraint("length(content) > 0", name="content_not_empty"),
        CheckConstraint("length(category) > 0", name="category_not_empty"),
    )
