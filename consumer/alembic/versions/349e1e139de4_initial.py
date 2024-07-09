"""initial

Revision ID: 349e1e139de4
Revises: 
Create Date: 2024-07-09 10:55:51.113197

"""
from typing import Sequence, Union
from models import Base, Event, EventProperty
from db import engine

# revision identifiers, used by Alembic.
revision: str = '349e1e139de4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

tables = [Event.__table__, EventProperty.__table__]

def upgrade() -> None:
    Base.metadata.create_all(engine, tables=tables)


def downgrade() -> None:
    Base.metadata.drop_all(engine, tables=tables)
