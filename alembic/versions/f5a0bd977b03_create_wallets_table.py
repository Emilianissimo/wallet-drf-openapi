"""create wallets table

Revision ID: f5a0bd977b03
Revises: 
Create Date: 2023-10-20 20:38:54.642084

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5a0bd977b03'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'wallets',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('label', sa.String(length=255), nullable=False),
        sa.Column('balance', sa.DECIMAL(precision=18, scale=2), nullable=True, default="0.00"),
        sa.Column('created_at', sa.DateTime(timezone=True), default=datetime.now),
        sa.Column('updated_at', sa.DateTime(timezone=True), default=datetime.now),
    )
    op.create_index(op.f('ix_wallets_id'), 'wallets', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_wallets_id'), table_name='wallets')
    op.drop_table('wallets')
