"""empty message

Revision ID: 906d67286293
Revises: 2cec11982f6a
Create Date: 2022-11-19 17:51:26.412866

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '906d67286293'
down_revision = '2cec11982f6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('request_statuses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('request_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('incidents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject', sa.String(length=64), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('priority', sa.Integer(), nullable=True),
    sa.Column('criticality', sa.Integer(), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.Column('responsible_employee_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['responsible_employee_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['request_statuses.id'], ),
    sa.ForeignKeyConstraint(['type_id'], ['request_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('incidents')
    op.drop_table('request_types')
    op.drop_table('request_statuses')
    # ### end Alembic commands ###
