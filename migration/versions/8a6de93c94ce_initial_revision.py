"""initial revision

Revision ID: 8a6de93c94ce
Revises: 0e835fdce86a
Create Date: 2025-07-08 12:30:50.404217

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = '8a6de93c94ce'
down_revision = '0e835fdce86a'
branch_labels = None
depends_on = None


def get_foreign_key_name(table_name, column_name):
    """Get foreign key constraint name for given table and column"""
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)

    for fk in inspector.get_foreign_keys(table_name):
        if column_name in fk['constrained_columns']:
            return fk['name']
    return None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)

    # Disable foreign keys for SQLite
    op.execute('PRAGMA foreign_keys = OFF;')

    # Clean up any leftover temporary tables
    temp_tables = [
        '_alembic_tmp_services',
        '_alembic_tmp_services_availability',
        '_alembic_tmp_subscription_services'
    ]

    for table in temp_tables:
        if table in inspector.get_table_names():
            op.drop_table(table)

    # Create new junction table if not exists
    if 'subscription_services' not in inspector.get_table_names():
        op.create_table(
            'subscription_services',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('service_id', sa.Integer, sa.ForeignKey('services.id')),
            sa.Column('subscription_id', sa.Integer, sa.ForeignKey('subscriptions.id')),
            sa.Column('quantity', sa.Integer)
        )

    # Rebuild services table without subscription_id and quantity
    if 'services' in inspector.get_table_names():
        # Create new table with correct structure
        op.create_table(
            'services_new',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('category_id', sa.Integer, sa.ForeignKey('categories.id')),
            sa.Column('description', sa.String(50), nullable=False),
            sa.Column('price', sa.Integer, nullable=False),
        )

        # Copy data from old table
        op.execute('''
            INSERT INTO services_new (id, category_id, description, price)
            SELECT id, category_id, description, price FROM services
        ''')

        # Remove old table
        op.drop_table('services')

        # Rename new table
        op.rename_table('services_new', 'services')

    # Rebuild services_availability table with new FK
    if 'services_availability' in inspector.get_table_names():
        # Create new table with correct structure
        op.create_table(
            'services_availability_new',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('client_id', sa.Integer, sa.ForeignKey('clients.id')),
            sa.Column('service_id', sa.Integer, sa.ForeignKey('subscription_services.id')),
            sa.Column('quantity', sa.Integer, nullable=False),
        )

        # For data migration: we can't automatically convert, so data will be lost
        # If you need to preserve data, add custom migration logic here

        # Remove old table
        op.drop_table('services_availability')

        # Rename new table
        op.rename_table('services_availability_new', 'services_availability')
    else:
        # Create table if it didn't exist
        op.create_table(
            'services_availability',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('client_id', sa.Integer, sa.ForeignKey('clients.id')),
            sa.Column('service_id', sa.Integer, sa.ForeignKey('subscription_services.id')),
            sa.Column('quantity', sa.Integer, nullable=False),
        )

    # Re-enable foreign keys
    op.execute('PRAGMA foreign_keys = ON;')


def downgrade() -> None:
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)

    # Disable foreign keys for SQLite
    op.execute('PRAGMA foreign_keys = OFF;')

    # Clean up any leftover temporary tables
    temp_tables = [
        '_alembic_tmp_services',
        '_alembic_tmp_services_availability',
        '_alembic_tmp_subscription_services'
    ]

    for table in temp_tables:
        if table in inspector.get_table_names():
            op.drop_table(table)

    # Revert services_availability table
    if 'services_availability' in inspector.get_table_names():
        op.create_table(
            'services_availability_old',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('client_id', sa.Integer, sa.ForeignKey('clients.id')),
            sa.Column('service_id', sa.Integer, sa.ForeignKey('services.id')),
            sa.Column('quantity', sa.Integer, nullable=False),
        )

        op.drop_table('services_availability')
        op.rename_table('services_availability_old', 'services_availability')

    # Revert services table
    if 'services' in inspector.get_table_names():
        op.create_table(
            'services_old',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('category_id', sa.Integer, sa.ForeignKey('categories.id')),
            sa.Column('description', sa.String(50), nullable=False),
            sa.Column('price', sa.Integer, nullable=False),
            sa.Column('subscription_id', sa.Integer, sa.ForeignKey('subscriptions.id')),
            sa.Column('quantity', sa.Integer),
        )

        # Copy data back
        op.execute('''
            INSERT INTO services_old (id, category_id, description, price)
            SELECT id, category_id, description, price FROM services
        ''')

        op.drop_table('services')
        op.rename_table('services_old', 'services')

    # Drop junction table
    if 'subscription_services' in inspector.get_table_names():
        op.drop_table('subscription_services')

    # Re-enable foreign keys
    op.execute('PRAGMA foreign_keys = ON;')
