"""Alter post datetime column for social media

Revision ID: 3ddc74880a74
Revises: 60c1642c7d81
Create Date: 2025-12-04 11:26:32.078742

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ddc74880a74'
down_revision: Union[str, Sequence[str], None] = '60c1642c7d81'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    ALTER TABLE social_media_posts
RENAME COLUMN post_datetime TO posted_datetime;           
    """)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
   ALTER TABLE social_media_posts
RENAME COLUMN posted_datetime TO post_datetime;           
    """)
    pass
