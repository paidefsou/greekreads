"""Add columns read/rating/created at books table

Revision ID: c2530d271ccb
Revises: 8ca1fe673aad
Create Date: 2022-11-13 22:50:29.332937

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2530d271ccb'
down_revision = '8ca1fe673aad'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('books', sa.Column(
        'read', sa.Boolean(), nullable=False, server_default='FALSE'),)
    op.add_column('books', sa.Column(
        'rating', sa.Integer(), nullable=False))
    op.add_column('books', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('books', 'read')
    op.drop_column('books', 'rating')
    op.drop_column('books', 'created_at')
    pass
