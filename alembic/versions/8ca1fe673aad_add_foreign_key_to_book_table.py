"""Add foreign key to book table

Revision ID: 8ca1fe673aad
Revises: 722c31abc5c4
Create Date: 2022-11-13 22:45:34.990679

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ca1fe673aad'
down_revision = '722c31abc5c4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('books', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('book_users_fk', source_table="books", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('book_users_fk', table_name="books")
    op.drop_column('books', 'owner_id')
    pass
