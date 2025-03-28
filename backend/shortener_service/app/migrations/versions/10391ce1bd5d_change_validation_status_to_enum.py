"""Change validation status to enum

Revision ID: 10391ce1bd5d
Revises: 84acfcb696e0
Create Date: 2025-03-28 19:34:52.635837

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10391ce1bd5d'
down_revision: Union[str, None] = '84acfcb696e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    validation_status_enum = sa.Enum('PENDING', 'VALID', 'INVALID', name='validationstatus')
    validation_status_enum.create(op.get_bind(), checkfirst=True)

    op.drop_column('shortened_urls', 'is_valid')

    op.add_column(
        'shortened_urls',
        sa.Column(
            'validation_status',
            validation_status_enum,
            nullable=False,
            server_default='PENDING'
        )
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('shortened_urls', 'validation_status')

    op.add_column(
        'shortened_urls',
        sa.Column(
            'is_valid',
            sa.BOOLEAN(),
            nullable=False,
            server_default=sa.false()
        )
    )

    validation_status_enum = sa.Enum('PENDING', 'VALID', 'INVALID', name='validationstatus')
    validation_status_enum.drop(op.get_bind(), checkfirst=True)

