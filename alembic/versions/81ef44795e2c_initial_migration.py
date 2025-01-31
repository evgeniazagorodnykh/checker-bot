"""Initial migration

Revision ID: 81ef44795e2c
Revises: 
Create Date: 2025-01-31 12:42:06.235104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '81ef44795e2c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # ### end Alembic commands ###
    pass


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('sent_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('read', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('read_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('sender_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('receiver_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('delivered', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['receiver_id'], ['user.id'], name='message_receiver_id_fkey'),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], name='message_sender_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='message_pkey')
    )
    op.create_index('ix_message_id', 'message', ['id'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(length=320), autoincrement=False, nullable=False),
    sa.Column('username', sa.VARCHAR(length=320), autoincrement=False, nullable=False),
    sa.Column('registered_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('hashed_password', sa.VARCHAR(length=1024), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('is_superuser', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('is_verified', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('telegram_id', sa.VARCHAR(length=320), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('telegram_id', name='user_telegram_id_key')
    )
    op.create_index('ix_user_username', 'user', ['username'], unique=True)
    op.create_index('ix_user_id', 'user', ['id'], unique=False)
    op.create_index('ix_user_email', 'user', ['email'], unique=True)
    # ### end Alembic commands ###
