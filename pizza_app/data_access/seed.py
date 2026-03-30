"""Database seeding helpers.

We insert a small pizza menu (5-10 typical pizzas) on first start.
"""

from __future__ import annotations

from sqlmodel import Session

from ..domain.models import Pizza


class MenuSeeder:
    """Seeds the database with a default pizza menu."""

    def seed(self, session: Session) -> None:
        """Insert a default pizza menu (id autoincrement)."""
        pizzas = [
            Pizza(name="Margherita", price_chf=14.50, ingredients="Tomato, mozzarella, basil"),
            Pizza(name="Funghi", price_chf=16.50, ingredients="Tomato, mozzarella, mushrooms"),
            Pizza(name="Prosciutto", price_chf=17.50, ingredients="Tomato, mozzarella, ham"),
            Pizza(name="Salami", price_chf=17.50, ingredients="Tomato, mozzarella, salami"),
            Pizza(name="Quattro Stagioni", price_chf=19.50, ingredients="Ham, mushrooms, artichokes, olives"),
            Pizza(name="Quattro Formaggi", price_chf=19.50, ingredients="Mozzarella, gorgonzola, parmesan, fontina"),
            Pizza(name="Hawaii", price_chf=18.50, ingredients="Ham, pineapple"),
            Pizza(name="Diavola", price_chf=19.00, ingredients="Spicy salami, chili"),
            Pizza(name="Tonno e Cipolla", price_chf=18.00, ingredients="Tuna, onion"),
            Pizza(name="Vegetariana", price_chf=18.50, ingredients="Mixed vegetables"),
        ]
        for p in pizzas:
            session.add(p)
