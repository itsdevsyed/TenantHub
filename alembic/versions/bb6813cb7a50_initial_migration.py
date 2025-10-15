"""Initial migration

Revision ID: bb6813cb7a50
Revises: 513b90012fd0
Create Date: 2025-10-15 21:24:20.802998

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb6813cb7a50'
down_revision: Union[str, Sequence[str], None] = '513b90012fd0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
