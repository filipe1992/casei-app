"""melhorias necessarias para uso de email

Revision ID: 654d4e8893c8
Revises: c094017991ad
Create Date: 2025-06-18 10:40:07.302822

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '654d4e8893c8'
down_revision: Union[str, None] = 'c094017991ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email_confirmed', sa.Boolean(), nullable=True, default=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'email_confirmed')
    # ### end Alembic commands ###
