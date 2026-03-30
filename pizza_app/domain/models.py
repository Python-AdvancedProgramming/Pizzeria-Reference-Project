"""Domain and ORM models.

We use SQLModel (SQLAlchemy + Pydantic) to map domain objects to a SQLite database.

Tables:
- Pizza: menu items
- Order: transaction header (timestamp, totals)
- OrderItem: line items for an Order (pizza + quantity + pricing snapshot)
"""

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class Pizza(SQLModel, table=True):
    """A menu pizza.

    Note: This is both a domain object and an ORM model. For a bigger system you might
    separate pure domain models from persistence models, but for this exercise a combined
    model keeps things readable.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, min_length=2, max_length=60)
    price_chf: float = Field(gt=0, le=100)
    ingredients: str = Field(default="", max_length=200)

    order_items: list["OrderItem"] = Relationship(back_populates="pizza")


class Order(SQLModel, table=True):
    """An order/transaction."""

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)

    subtotal_chf: float = Field(default=0.0, ge=0)
    discount_chf: float = Field(default=0.0, ge=0)
    total_chf: float = Field(default=0.0, ge=0)

    items: list["OrderItem"] = Relationship(back_populates="order")


class OrderItem(SQLModel, table=True):
    """One line item within an order."""

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id", index=True)
    pizza_id: int = Field(foreign_key="pizza.id", index=True)

    quantity: int = Field(ge=1, le=99)
    unit_price_chf: float = Field(gt=0, le=100)  # snapshot at time of purchase
    line_total_chf: float = Field(default=0.0, ge=0)

    order: "Order" = Relationship(back_populates="items")
    pizza: "Pizza" = Relationship(back_populates="order_items")
