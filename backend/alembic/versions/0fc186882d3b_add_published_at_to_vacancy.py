"""add published_at to vacancy

Revision ID: 0fc186882d3b
Revises:
Create Date: 2025-03-13 11:03:19.272355

"""
from typing import Sequence, Union
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '0fc186882d3b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("CREATE SEQUENCE IF NOT EXISTS vacancy_id_seq")
    op.execute("ALTER TABLE vacancies ALTER COLUMN id SET DEFAULT nextval('vacancy_id_seq')")
    op.execute("SELECT setval('vacancy_id_seq', (SELECT MAX(id) FROM vacancies))")


def downgrade():
    op.execute("ALTER TABLE vacancies ALTER COLUMN id DROP DEFAULT")
    op.execute("DROP SEQUENCE IF EXISTS vacancy_id_seq")
