"""create transactions table

Revision ID: 076a4a78f294
Revises: f5a0bd977b03
Create Date: 2023-10-20 20:39:00.357368

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '076a4a78f294'
down_revision: Union[str, None] = 'f5a0bd977b03'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('txid', sa.String(length=36), nullable=True),
        sa.Column('amount', sa.DECIMAL(precision=18, scale=2), nullable=True),
        sa.Column('wallet_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['wallet_id'], ['wallets.id']),
        sa.Column('transaction_type', sa.Boolean, default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), default=datetime.now),
        sa.Column('updated_at', sa.DateTime(timezone=True), default=datetime.now),
    )
    op.create_index(op.f('ix_transactions_id'), 'transactions', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_transactions_id'), table_name='transactions')
    op.drop_table('transactions')
