"""nova atualizaçao no no guest agora so pode ter um album

Revision ID: b1826036274a
Revises: b47bb1574707
Create Date: 2025-06-07 10:20:13.453055

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b1826036274a'
down_revision: Union[str, None] = 'b47bb1574707'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
