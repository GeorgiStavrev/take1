"""Adds unique constraint

Revision ID: 066fca5be5a9
Revises: b2ecc00d87d5
Create Date: 2024-07-11 16:17:05.846136

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '066fca5be5a9'
down_revision: Union[str, None] = 'b2ecc00d87d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('uc__user_prop', 'user_properties', ['client_id', 'user_id', 'name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uc__user_prop', 'user_properties', type_='unique')
    # ### end Alembic commands ###