"""empty message

Revision ID: e44f9681604a
Revises: 
Create Date: 2017-10-31 18:18:15.341060

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e44f9681604a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('avatar', sa.String(length=256), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('tokens', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('email', name=op.f('uq_users_email'))
    )
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], name=op.f('fk_category_created_by_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_category'))
    )
    op.create_table('item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], name=op.f('fk_item_category_id_category')),
    sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], name=op.f('fk_item_created_by_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_item'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('item')
    op.drop_table('category')
    op.drop_table('users')
    # ### end Alembic commands ###
