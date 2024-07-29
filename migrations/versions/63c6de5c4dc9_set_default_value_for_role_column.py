"""Set default value for role column

Revision ID: 63c6de5c4dc9
Revises: 719afd9caa60
Create Date: 2024-07-29 23:16:59.840524

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63c6de5c4dc9'
down_revision = '719afd9caa60'
branch_labels = None
depends_on = None


def upgrade():
    # Set the default value for the role column
    with op.batch_alter_table('user') as batch_op:
        batch_op.alter_column('role', existing_type=sa.String(length=50), nullable=False, server_default='user')


def downgrade():
    # Remove the default value for the role column
    with op.batch_alter_table('user') as batch_op:
        batch_op.alter_column('role', existing_type=sa.String(length=50), nullable=False, server_default=None)
