"""create currency information table

Revision ID: 55c70cc8f20c
Revises: None
Create Date: 2020-02-02 16:14:01.486966

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as postgresql


# revision identifiers, used by Alembic.
revision = '55c70cc8f20c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'currency_information',
        sa.Column('base_currency', sa.String(3), nullable=False),
        sa.Column('changes', postgresql.JSONB, nullable=False),
        sa.Column('change_date', sa.Date, nullable=False),
        sa.Column('retrieved_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False, unique=True, server_default=sa.func.now()),
    )

    op.create_unique_constraint('uq_currency_information_change_date_retrieved_at', 'currency_information', ['change_date', 'retrieved_at'])

    op.create_index('ik_currency_information_change_date', 'currency_information', ['change_date'])


def downgrade():
    op.drop_index('ik_currency_information_change_date', 'currency_information')
    op.drop_constraint('uq_currency_information_change_date_retrieved_at', 'currency_information')
    op.drop_table('currency_information')
