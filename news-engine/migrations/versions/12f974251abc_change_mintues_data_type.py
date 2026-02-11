"""Change Mintues Data type

Revision ID: 12f974251abc
Revises: 50618a7aa4b4
Create Date: 2025-10-15 11:02:37.396953

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12f974251abc'
down_revision: Union[str, Sequence[str], None] = '50618a7aa4b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        
    DO $$
    BEGIN
        IF (SELECT data_type FROM information_schema.columns
            WHERE table_name = 'player_abroads'
            AND column_name = 'minutes_played') <> 'text' THEN

            -- Clean up non-numeric entries first
            DELETE FROM player_abroads
            WHERE minutes_played::text !~ '^[0-9]+$';

            ALTER TABLE player_abroads
            ALTER COLUMN minutes_played TYPE text
            USING minutes_played::text,
            ALTER COLUMN minutes_played SET DEFAULT NULL;
        END IF;
    END $$;
    ''')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
    DO $$
    BEGIN
        IF (SELECT data_type FROM information_schema.columns
            WHERE table_name = 'player_abroads'
            AND column_name = 'minutes_played') <> 'integer' THEN

            ALTER TABLE player_abroads
            ALTER COLUMN minutes_played DROP DEFAULT,
            ALTER COLUMN minutes_played TYPE integer
            USING minutes_played::integer,
            ALTER COLUMN minutes_played SET DEFAULT NULL;
        END IF;
    END $$;
    ''')
    pass
