"""Alter name in  teams test table

Revision ID: 9ef301a248f0
Revises: 12f974251abc
Create Date: 2025-10-15 16:32:54.547534

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ef301a248f0'
down_revision: Union[str, Sequence[str], None] = '12f974251abc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
    DO $$
    BEGIN
        IF (SELECT data_type FROM information_schema.columns
            WHERE table_name = 'teams_test'
            AND column_name = 'name') <> 'text' THEN
               
            ALTER TABLE teams_test
            ALTER COLUMN name DROP DEFAULT,
            ALTER COLUMN name TYPE text USING name::text,
            ALTER COLUMN name SET DEFAULT NULL;
        END IF;
    END $$;
               
    DO $$
    BEGIN
        -- Only run if the column is not already bigint
        IF (SELECT data_type 
            FROM information_schema.columns
            WHERE table_name = 'teams_test'
            AND column_name = 'id') <> 'bigint' THEN

            -- Step 1: Alter column type to bigint
            ALTER TABLE teams_test
            ALTER COLUMN id TYPE bigint;

            -- Step 2: Create a sequence if it does not exist
            IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relkind='S' AND relname='teams_test_id_seq') THEN
                CREATE SEQUENCE teams_test_id_seq;
            END IF;

            -- Step 3: Attach the sequence to the column
            ALTER TABLE teams_test
            ALTER COLUMN id SET DEFAULT nextval('teams_test_id_seq');
        END IF;
    END $$;

    ''')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
    DO $$
    BEGIN
        -- Only run if column is not already character(1)
        IF (SELECT data_type 
            FROM information_schema.columns
            WHERE table_name = 'teams_test'
            AND column_name = 'name') <> 'character' THEN

            -- Optional: Replace values longer than 1 character or handle NULLs
            UPDATE teams_test
            SET name = substring(name from 1 for 1)
            WHERE name IS NOT NULL;

            -- Alter column type and allow NULLs
            ALTER TABLE teams_test
            ALTER COLUMN name DROP DEFAULT,
            ALTER COLUMN name TYPE character(1) USING name::char(1),
            ALTER COLUMN name SET DEFAULT NULL;
        END IF;
    END $$;
               
    DO $$
    BEGIN
        -- Only run if the column is currently bigint
        IF (SELECT data_type 
            FROM information_schema.columns
            WHERE table_name = 'teams_test'
            AND column_name = 'id') = 'bigint' THEN

            -- Step 1: Remove default sequence
            ALTER TABLE teams_test
            ALTER COLUMN id DROP DEFAULT;

            -- Step 2: Alter column type back to integer
            ALTER TABLE teams_test
            ALTER COLUMN id TYPE integer USING id::integer;

            -- Step 3: Drop sequence if exists
            IF EXISTS (SELECT 1 FROM pg_class WHERE relkind='S' AND relname='teams_test_id_seq') THEN
                DROP SEQUENCE teams_test_id_seq;
            END IF;
        END IF;
    END $$;
    ''')
    pass
