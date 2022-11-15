"""Create books table

Revision ID: e29c4e253e90
Revises: 
Create Date: 2022-11-13 22:07:31.734566

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e29c4e253e90'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op. create_table('books', sa.Column('id', sa.Integer(), nullable=False, primary_key=True)
                     , sa.Column('title', sa.String(), nullable=False))
    pass

def downgrade() -> None:
    op.drop_table('books')
    pass
