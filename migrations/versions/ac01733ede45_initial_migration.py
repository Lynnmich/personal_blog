"""Initial Migration

Revision ID: ac01733ede45
Revises: 
Create Date: 2023-07-05 13:03:16.536346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac01733ede45'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('admin_name', sa.String(length=20), nullable=False),
    sa.Column('date_added', sa.Date(), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('admin_name'),
    sa.UniqueConstraint('email')
    )
    op.create_table('destinations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('date_posted', sa.Date(), nullable=True),
    sa.Column('content', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('subtitle', sa.String(length=200), nullable=False),
    sa.Column('date_posted', sa.Date(), nullable=True),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('slug', sa.String(length=200), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    op.drop_table('destinations')
    op.drop_table('admin')
    # ### end Alembic commands ###
