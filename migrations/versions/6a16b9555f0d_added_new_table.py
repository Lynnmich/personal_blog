"""Added new table

Revision ID: 6a16b9555f0d
Revises: 48e690eec949
Create Date: 2023-07-02 13:35:36.427020

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a16b9555f0d'
down_revision = '48e690eec949'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_posts')
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.alter_column('date_added',
               existing_type=sa.DATETIME(),
               type_=sa.Date(),
               existing_nullable=True)
        batch_op.alter_column('password_hash',
               existing_type=sa.VARCHAR(length=128),
               type_=sa.String(length=20),
               existing_nullable=False)
        batch_op.create_unique_constraint(None, ['email'])

    with op.batch_alter_table('destinations', schema=None) as batch_op:
        batch_op.alter_column('date_posted',
               existing_type=sa.DATETIME(),
               type_=sa.Date(),
               existing_nullable=True)

    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.alter_column('date_posted',
               existing_type=sa.DATETIME(),
               type_=sa.Date(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.alter_column('date_posted',
               existing_type=sa.Date(),
               type_=sa.DATETIME(),
               existing_nullable=True)

    with op.batch_alter_table('destinations', schema=None) as batch_op:
        batch_op.alter_column('date_posted',
               existing_type=sa.Date(),
               type_=sa.DATETIME(),
               existing_nullable=True)

    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('password_hash',
               existing_type=sa.String(length=20),
               type_=sa.VARCHAR(length=128),
               existing_nullable=False)
        batch_op.alter_column('date_added',
               existing_type=sa.Date(),
               type_=sa.DATETIME(),
               existing_nullable=True)

    op.create_table('_alembic_tmp_posts',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=200), nullable=True),
    sa.Column('subtitle', sa.VARCHAR(length=200), nullable=True),
    sa.Column('date_posted', sa.DATETIME(), nullable=True),
    sa.Column('content', sa.TEXT(), nullable=True),
    sa.Column('slug', sa.VARCHAR(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###