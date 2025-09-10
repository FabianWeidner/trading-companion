"""create trades table

Revision ID: e508e87eff07
Revises:
Create Date: 2025-09-10 11:57:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e508e87eff07"
down_revision = None  # <- ganz wichtig: keine Vorgänger-Revision
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "trades",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("symbol", sa.String(20), nullable=False, index=True),
        sa.Column("side", sa.String(4), nullable=False),
        sa.Column("strategy", sa.String(50), nullable=False, index=True),
        sa.Column("qty", sa.Float, nullable=False),
        sa.Column("price", sa.Float, nullable=False),
        sa.Column("opened_at", sa.DateTime, nullable=False),
        sa.Column("screenshot_url", sa.String(255), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("trades")
