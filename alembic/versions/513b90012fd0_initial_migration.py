"""Initial migration

Revision ID: 513b90012fd0
Revises: f8f6c6272a38
Create Date: 2025-10-15 21:21:42.253233

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '513b90012fd0'
down_revision: Union[str, Sequence[str], None] = 'f8f6c6272a38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
