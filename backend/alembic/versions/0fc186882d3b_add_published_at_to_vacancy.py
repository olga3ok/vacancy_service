"""add published_at to vacancy

Revision ID: 0fc186882d3b
Revises: 
Create Date: 2025-03-13 11:03:19.272355

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0fc186882d3b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('vacancies', sa.Column('published_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('vacancies') as batch_op:
        batch_op.drop_column('published_at')
