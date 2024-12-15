"""Update null processed values

Revision ID: update_null_processed
Revises: bc4f4106061a
Create Date: 2024-12-15 14:10:16.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'update_null_processed'
down_revision: Union[str, None] = 'bc4f4106061a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 创建新表
    op.execute("""
        CREATE TABLE messages_new (
            id INTEGER PRIMARY KEY,
            title VARCHAR NOT NULL,
            content VARCHAR NOT NULL,
            category VARCHAR NOT NULL,
            is_read BOOLEAN NOT NULL DEFAULT false,
            processed BOOLEAN NOT NULL DEFAULT false,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 复制数据
    op.execute("""
        INSERT INTO messages_new 
        SELECT id, title, content, category, 
               COALESCE(is_read, false) as is_read, 
               COALESCE(processed, false) as processed,
               created_at, updated_at
        FROM messages
    """)
    
    # 删除旧表
    op.execute("DROP TABLE messages")
    
    # 重命名新表
    op.execute("ALTER TABLE messages_new RENAME TO messages")
    
    # 重新创建索引
    op.execute("CREATE INDEX ix_messages_title ON messages (title)")
    op.execute("CREATE INDEX ix_messages_category ON messages (category)")
    op.execute("CREATE INDEX ix_messages_processed ON messages (processed)")


def downgrade() -> None:
    # 创建新表（允许 NULL 值）
    op.execute("""
        CREATE TABLE messages_new (
            id INTEGER PRIMARY KEY,
            title VARCHAR NOT NULL,
            content VARCHAR NOT NULL,
            category VARCHAR NOT NULL,
            is_read BOOLEAN,
            processed BOOLEAN,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 复制数据
    op.execute("""
        INSERT INTO messages_new 
        SELECT * FROM messages
    """)
    
    # 删除旧表
    op.execute("DROP TABLE messages")
    
    # 重命名新表
    op.execute("ALTER TABLE messages_new RENAME TO messages")
    
    # 重新创建索引
    op.execute("CREATE INDEX ix_messages_title ON messages (title)")
    op.execute("CREATE INDEX ix_messages_category ON messages (category)")
    op.execute("CREATE INDEX ix_messages_processed ON messages (processed)")
