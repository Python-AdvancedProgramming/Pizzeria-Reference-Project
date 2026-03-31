"""DAO classes for persistence.

The rest of the application should not know about raw SQL/ORM sessions.
DAOs encapsulate CRUD operations and queries behind class-based interfaces.
"""

from __future__ import annotations

from typing import List, Optional

from sqlalchemy.engine import Engine
from sqlmodel import Session, select

from ..domain.models import Order, Pizza


class BaseDAO:
    """Base class holding the SQLAlchemy/SQLModel engine."""

    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def session(self) -> Session:
        """Create a new database session."""
        return Session(self.engine)


class PizzaDAO(BaseDAO):
    """DAO for read access to pizzas/menu data."""

    def list_menu(self) -> List[Pizza]:
        """Return all pizzas sorted by name."""
        with self.session() as session:
            return list(session.exec(select(Pizza).order_by(Pizza.name)).all())

    def get_by_id(self, pizza_id: int) -> Optional[Pizza]:
        """Get a single pizza by id."""
        with self.session() as session:
            return session.get(Pizza, pizza_id)


class OrderDAO(BaseDAO):
    """DAO for order header and order item persistence."""

    def create(self, order: Order) -> Order:
        """Persist an Order and return the stored order, with items and pizzas eagerly loaded."""
        with self.session() as session:
            session.add(order)
            session.commit()
            session.refresh(order)
        return order
    
    def list_recent(self, limit: int = 200) -> List[Order]:
        """Return orders newest-first."""
        with self.session() as session:
            statement = select(Order).order_by(Order.created_at.desc()).limit(limit)
            return list(session.exec(statement).all())

    def get_with_items(self, order_id: int) -> Optional[Order]:
        """Load an order together with its items and pizzas."""
        with self.session() as session:
            order = session.get(Order, order_id)
            if not order:
                return None
            _ = list(order.items)
            for item in order.items:
                _ = item.pizza
            return order
