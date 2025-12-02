"""add_org_type_and_new_tables

Revision ID: 89d63a900646
Revises: 4374dad262ef
Create Date: 2025-12-02 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '89d63a900646'
down_revision: Union[str, None] = '2f122fa1dde6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create ENUM type for org_type (only if it doesn't exist)
    # Check if enum already exists in database
    connection = op.get_bind()
    result = connection.execute(sa.text(
        "SELECT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'org_type_enum')"
    ))
    enum_exists = result.scalar()

    if not enum_exists:
        org_type_enum = postgresql.ENUM('banking', 'telecom', 'ecommerce', name='org_type_enum', create_type=True)
        org_type_enum.create(connection, checkfirst=False)

    # Add org_type column to organizations table with default 'telecom'
    # Check if column already exists
    result = connection.execute(sa.text(
        "SELECT EXISTS (SELECT 1 FROM information_schema.columns "
        "WHERE table_name = 'organizations' AND column_name = 'org_type')"
    ))
    column_exists = result.scalar()

    if not column_exists:
        op.add_column('organizations',
            sa.Column('org_type',
                      postgresql.ENUM('banking', 'telecom', 'ecommerce', name='org_type_enum', create_type=False),
                      nullable=False,
                      server_default='telecom')
        )
        # Update existing organizations to 'telecom'
        op.execute("UPDATE organizations SET org_type = 'telecom' WHERE org_type IS NULL")

    # Create customer_segments table
    op.create_table('customer_segments',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('customer_id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('segment', sa.String(), nullable=False),
        sa.Column('segment_score', sa.Numeric(5, 2), nullable=False),  # 0.00 to 100.00
        sa.Column('rfm_category', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('churn_risk_level', sa.String(), nullable=False),  # 'Low', 'Medium', 'High', 'Critical'
        sa.Column('assigned_at', sa.DateTime(), nullable=False),
        sa.Column('extra_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customer_segments_id'), 'customer_segments', ['id'], unique=False)
    op.create_index(op.f('ix_customer_segments_customer_id'), 'customer_segments', ['customer_id'], unique=False)
    op.create_index(op.f('ix_customer_segments_organization_id'), 'customer_segments', ['organization_id'], unique=False)
    op.create_index(op.f('ix_customer_segments_segment'), 'customer_segments', ['segment'], unique=False)

    # Create behavior_analysis table
    # Use postgresql.ENUM with create_type=False to reference existing ENUM
    op.create_table('behavior_analysis',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('customer_id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('org_type', postgresql.ENUM('banking', 'telecom', 'ecommerce', name='org_type_enum', create_type=False), nullable=False),
        sa.Column('behavior_score', sa.Numeric(5, 2), nullable=False),  # 0.00 to 100.00
        sa.Column('activity_trend', sa.String(), nullable=True),  # 'increasing', 'stable', 'declining'
        sa.Column('value_trend', sa.String(), nullable=True),
        sa.Column('engagement_trend', sa.String(), nullable=True),
        sa.Column('risk_signals', postgresql.JSONB(astext_type=sa.Text()), nullable=True),  # Array of risk signals
        sa.Column('recommendations', postgresql.JSONB(astext_type=sa.Text()), nullable=True),  # Array of recommendations
        sa.Column('analyzed_at', sa.DateTime(), nullable=False),
        sa.Column('extra_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_behavior_analysis_id'), 'behavior_analysis', ['id'], unique=False)
    op.create_index(op.f('ix_behavior_analysis_customer_id'), 'behavior_analysis', ['customer_id'], unique=False)
    op.create_index(op.f('ix_behavior_analysis_organization_id'), 'behavior_analysis', ['organization_id'], unique=False)


def downgrade() -> None:
    # Drop tables
    op.drop_index(op.f('ix_behavior_analysis_organization_id'), table_name='behavior_analysis')
    op.drop_index(op.f('ix_behavior_analysis_customer_id'), table_name='behavior_analysis')
    op.drop_index(op.f('ix_behavior_analysis_id'), table_name='behavior_analysis')
    op.drop_table('behavior_analysis')

    op.drop_index(op.f('ix_customer_segments_segment'), table_name='customer_segments')
    op.drop_index(op.f('ix_customer_segments_organization_id'), table_name='customer_segments')
    op.drop_index(op.f('ix_customer_segments_customer_id'), table_name='customer_segments')
    op.drop_index(op.f('ix_customer_segments_id'), table_name='customer_segments')
    op.drop_table('customer_segments')

    # Drop org_type column
    op.drop_column('organizations', 'org_type')

    # Drop ENUM type
    org_type_enum = postgresql.ENUM('banking', 'telecom', 'ecommerce', name='org_type_enum')
    org_type_enum.drop(op.get_bind(), checkfirst=True)
