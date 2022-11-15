"""Add author/desc column in books table

Revision ID: 8d5658a4e9fc
Revises: e29c4e253e90
Create Date: 2022-11-13 22:28:53.906795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d5658a4e9fc'
down_revision = 'e29c4e253e90'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('books', sa.Column('author', sa.String(), nullable=False))
    op.add_column('books', sa.Column('description', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('books', 'author')
    op.drop_column('books', 'description')
    pass
