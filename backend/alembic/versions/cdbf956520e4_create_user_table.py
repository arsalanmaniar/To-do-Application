"""Create user table

Revision ID: cdbf956520e4
Revises: 
Create Date: 2026-01-10 20:31:13.281640

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cdbf956520e4'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create the users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),

        # Primary key constraint
        sa.PrimaryKeyConstraint('id'),

        # Unique constraint for email
        sa.UniqueConstraint('email'),

        # Indexes
        sa.Index('ix_users_email', 'email', unique=True),
        sa.Index('ix_users_id', 'id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop the users table
    op.drop_table('users')
