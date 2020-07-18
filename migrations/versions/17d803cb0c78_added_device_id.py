"""added device id

Revision ID: 17d803cb0c78
Revises: c8e70d1daa16
Create Date: 2020-07-18 21:03:49.731758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "17d803cb0c78"
down_revision = "c8e70d1daa16"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column("device_id", sa.String(), nullable=True))


def downgrade():
    op.drop_column("users", "device_id")
