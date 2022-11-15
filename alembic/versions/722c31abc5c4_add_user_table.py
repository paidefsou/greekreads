"""Add user table

Revision ID: 722c31abc5c4
Revises: 8d5658a4e9fc
Create Date: 2022-11-13 22:41:10.809363

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '722c31abc5c4'
down_revision = '8d5658a4e9fc'
branch_labels = None
depends_on = None


def upgrade() -> None:
     op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
     pass

def downgrade() -> None:
    op.drop_table('users')
    pass
