"""create prospecting sessions and logs tables

Revision ID: 002
Revises: 001
Create Date: 2026-07-08 17:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'prospecting_sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('industry', sa.String(), nullable=False),
        sa.Column('location', sa.String(), nullable=False),
        sa.Column('max_companies', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(), nullable=False, server_default='pending'),
        sa.Column('progress', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('finished_at', sa.DateTime(), nullable=True),
    )

    op.create_index('ix_prospecting_sessions_status', 'prospecting_sessions', ['status'])
    op.create_index('ix_prospecting_sessions_created_at', 'prospecting_sessions', ['created_at'])

    op.create_table(
        'prospecting_session_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('prospecting_sessions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('level', sa.String(), nullable=False, server_default='info'),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
    )

    op.create_index('ix_prospecting_session_logs_session_id', 'prospecting_session_logs', ['session_id'])


def downgrade() -> None:
    op.drop_index('ix_prospecting_session_logs_session_id', table_name='prospecting_session_logs')
    op.drop_table('prospecting_session_logs')
    op.drop_index('ix_prospecting_sessions_created_at', table_name='prospecting_sessions')
    op.drop_index('ix_prospecting_sessions_status', table_name='prospecting_sessions')
    op.drop_table('prospecting_sessions')
