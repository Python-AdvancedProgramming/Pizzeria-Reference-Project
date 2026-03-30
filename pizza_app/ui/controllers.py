"""UI controllers.

Controllers coordinate between the UI layer and DAO/services.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from ..domain.models import Order, OrderItem, Pizza
from ..data_access.dao import OrderDAO, PizzaDAO
from ..services.invoice import InvoiceService
from ..services.pricing import PricingService


class AdminController:
    """Controller for admin queries."""

    def __init__(self, order_dao: OrderDAO) -> None:
        self.order_dao = order_dao

    def list_transactions(self, limit: int = 200) -> List[Order]:
        """List most recent orders."""
        return self.order_dao.list_recent(limit=limit)


@dataclass
class CartLine:
    """Cart line for UI display and pricing."""

    pizza: Pizza
    quantity: int

    @property
    def unit_price_chf(self) -> float:
        return float(self.pizza.price_chf)

    @property
    def line_total_chf(self) -> float:
        return round(self.unit_price_chf * self.quantity, 2)


class OrderController:
    """Controller for the customer/staff flow: menu -> cart -> checkout."""

    def __init__(
        self,
        pizza_dao: PizzaDAO,
        order_dao: OrderDAO,
        pricing: PricingService,
        invoice: InvoiceService,
    ) -> None:
        self.pizza_dao = pizza_dao
        self.order_dao = order_dao
        self.pricing = pricing
        self.invoice = invoice
        self._cart: Dict[int, int] = {}

    def menu(self) -> List[Pizza]:
        """Return the pizza menu."""
        return self.pizza_dao.list_menu()

    def cart_lines(self) -> List[CartLine]:
        """Return current cart as a list of cart lines."""
        lines: List[CartLine] = []
        for pid, qty in sorted(self._cart.items()):
            pizza = self.pizza_dao.get_by_id(pid)
            if pizza is None:
                continue
            lines.append(CartLine(pizza=pizza, quantity=qty))
        return lines

    def set_quantity(self, pizza_id: int, quantity: int) -> None:
        """Set quantity for a given pizza.

        Validation:
            quantity must be between 0 and 99 (0 removes).
        """
        if quantity < 0 or quantity > 99:
            raise ValueError("Quantity must be between 0 and 99.")
        if quantity == 0:
            self._cart.pop(pizza_id, None)
            return

        if self.pizza_dao.get_by_id(pizza_id) is None:
            raise ValueError(f"Unknown pizza id: {pizza_id}")
        self._cart[pizza_id] = quantity

    def add_one(self, pizza_id: int) -> None:
        """Add one unit of a pizza to the cart."""
        current = self._cart.get(pizza_id, 0)
        self.set_quantity(pizza_id, min(current + 1, 99))

    def remove_one(self, pizza_id: int) -> None:
        """Remove one unit of a pizza from the cart."""
        current = self._cart.get(pizza_id, 0)
        self.set_quantity(pizza_id, max(current - 1, 0))

    def clear_cart(self) -> None:
        """Remove all cart items."""
        self._cart.clear()

    def totals(self) -> Tuple[float, float, float]:
        """Return (subtotal, discount, total) for the current cart."""
        line_totals = [line.line_total_chf for line in self.cart_lines()]
        return self.pricing.totals_from_lines(line_totals)

    def checkout(self) -> Tuple[Order, str]:
        """Persist the current cart as an order and generate an invoice."""
        lines = self.cart_lines()
        if not lines:
            raise ValueError("Cart is empty.")

        subtotal, discount, total = self.totals()
        order = Order(subtotal_chf=subtotal, discount_chf=discount, total_chf=total)

        items: List[OrderItem] = []
        for line in lines:
            items.append(
                OrderItem(
                    order_id=0,
                    pizza_id=line.pizza.id or 0,
                    quantity=line.quantity,
                    unit_price_chf=line.unit_price_chf,
                    line_total_chf=line.line_total_chf,
                )
            )

        order = self.order_dao.create(order, items)
        order_full = self.order_dao.get_with_items(order.id)  # type: ignore[arg-type]
        if order_full is None:
            order_full = order

        pdf_path = self.invoice.generate_pdf(order_full)
        self.clear_cart()
        return order_full, str(pdf_path)
