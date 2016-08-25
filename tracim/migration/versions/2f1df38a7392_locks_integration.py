"""Locks integration

Revision ID: 2f1df38a7392
Revises: b4b8d57b54e5
Create Date: 2016-08-25 23:36:40.517449

"""

# revision identifiers, used by Alembic.
revision = '2f1df38a7392'
down_revision = 'b4b8d57b54e5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'locks',
        sa.Column('token', sa.Unicode(1024), primary_key=True, unique=False, nullable=False),
        sa.Column('depth', sa.Unicode(8), nullable=False, default='infinity'),
        sa.Column('user_mail', sa.Unicode(255),
                  sa.ForeignKey('users.email', ondelete='CASCADE', onupdate='CASCADE'), nullable=False),
        sa.Column('xml_owner', sa.Unicode(1024), unique=False, nullable=False),
        sa.Column('url_resource', sa.Unicode(1024), unique=False, nullable=False),
        sa.Column('type', sa.Unicode(32), unique=False, nullable=False, default='write'),
        sa.Column('timeout', sa.Float, unique=False, nullable=False),
        sa.Column('expire', sa.DateTime, unique=False, nullable=False),
        sa.Column('scope', sa.Unicode(32), unique=False, nullable=False, default='exclusive')
    )

    op.create_table(
        'url2token',
        sa.Column('token', sa.Unicode(1024), primary_key=True, unique=False, nullable=False, default=''),
        sa.Column('path', sa.Unicode(1024), unique=False, nullable=False, default='')
    )

def downgrade():
    op.drop_table('url2token')
    op.drop_table('locks')

