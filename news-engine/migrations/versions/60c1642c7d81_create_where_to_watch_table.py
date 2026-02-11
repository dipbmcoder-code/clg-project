"""Create Where to Watch Table

Revision ID: 60c1642c7d81
Revises: 9ef301a248f0
Create Date: 2025-11-06 13:25:38.525300

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '60c1642c7d81'
down_revision: Union[str, Sequence[str], None] = '9ef301a248f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
    CREATE TABLE IF NOT EXISTS "public"."where_to_watch" (
        id SERIAL PRIMARY KEY,
        
        league_id INTEGER DEFAULT 0,
        league_name TEXT DEFAULT NULL,
        
        country_name TEXT DEFAULT NULL,
        country_code TEXT DEFAULT NULL,
        
        season_year INTEGER DEFAULT 0,
        season_start DATE DEFAULT NULL,
        season_end DATE DEFAULT NULL,
        season_current BOOLEAN DEFAULT FALSE,
        
        tv_channels JSONB DEFAULT NULL,
        scrap_date DATE DEFAULT NULL,

        is_posted BOOLEAN DEFAULT FALSE,
        posted_datetime TIMESTAMP DEFAULT NULL,
        website_ids JSONB DEFAULT NULL
    ) WITH (oids = false);

    """)

    # Create indexes for faster lookups
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_where_to_watch_league_id
            ON "public"."where_to_watch" (league_id);

        CREATE INDEX IF NOT EXISTS idx_where_to_watch_season_year
            ON "public"."where_to_watch" (season_year);

        CREATE INDEX IF NOT EXISTS idx_where_to_watch_is_posted
            ON "public"."where_to_watch" (is_posted);
    """)
    pass


def downgrade() -> None:
    """Downgrade schema."""

    # Drop indexes first (safe cleanup)
    op.execute("""
        DROP INDEX IF EXISTS idx_where_to_watch_league_id;
        DROP INDEX IF EXISTS idx_where_to_watch_season_year;
        DROP INDEX IF EXISTS idx_where_to_watch_is_posted;
    """)

    # Drop table
    op.execute("""
    DROP TABLE IF EXISTS "public"."where_to_watch";
    """)
    pass
