"""added text blob for bio

Revision ID: 4af3b46c6486
Revises: df961c5a2aeb
Create Date: 2021-07-09 11:28:46.502389

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4af3b46c6486'
down_revision = 'df961c5a2aeb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('bio', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'bio')
    # ### end Alembic commands ###