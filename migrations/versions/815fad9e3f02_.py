"""empty message

Revision ID: 815fad9e3f02
Revises: 
Create Date: 2018-10-27 14:30:17.838409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '815fad9e3f02'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mobile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('mac', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('room',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('paused', sa.Integer(), nullable=True),
    sa.Column('volume', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('song',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('artist', sa.String(length=64), nullable=True),
    sa.Column('link', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('CC',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('roomId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['roomId'], ['room.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('current_signals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mobileId', sa.Integer(), nullable=True),
    sa.Column('roomId', sa.Integer(), nullable=True),
    sa.Column('rssi', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['mobileId'], ['mobile.id'], ),
    sa.ForeignKeyConstraint(['roomId'], ['room.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('light',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('roomId', sa.Integer(), nullable=True),
    sa.Column('uuid', sa.Integer(), nullable=True),
    sa.Column('brightness', sa.Integer(), nullable=True),
    sa.Column('hue', sa.Integer(), nullable=True),
    sa.Column('saturation', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['roomId'], ['room.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('satellite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ip', sa.String(length=64), nullable=True),
    sa.Column('port', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('roomId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['roomId'], ['room.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('satellite')
    op.drop_table('light')
    op.drop_table('current_signals')
    op.drop_table('CC')
    op.drop_table('song')
    op.drop_table('room')
    op.drop_table('mobile')
    # ### end Alembic commands ###
