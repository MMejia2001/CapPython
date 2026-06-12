"""create orders tables"""

from alembic import op
import sqlalchemy as sa

revision = "0001_create_orders_tables"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=False),
        sa.Column("customer", sa.String(length=120), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
    )
    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("sku", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("unit_price", sa.Float(), nullable=False),
        sa.Column("qty", sa.Integer(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("order_items")
    op.drop_table("orders")
