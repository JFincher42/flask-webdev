"""Added user confirmation

Revision ID: 881bddb6081a
Revises: bada4731e1b0
Create Date: 2022-08-27 11:20:39.573567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '881bddb6081a'
down_revision = 'bada4731e1b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###
