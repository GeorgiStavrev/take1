"""add user properties table

Revision ID: ef10c32133bb
Revises: 349e1e139de4
Create Date: 2024-07-09 11:55:21.751594

"""
from typing import Sequence, Union
from models import Base, UserProperty
from db import engine


# revision identifiers, used by Alembic.
revision: str = 'ef10c32133bb'
down_revision: Union[str, None] = '349e1e139de4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

tables = [UserProperty.__table__]

def upgrade() -> None:
    Base.metadata.create_all(engine, tables=tables)


def downgrade() -> None:
    Base.metadata.drop_all(engine, tables=tables)
