from typing import List, Optional, Sequence, Tuple

from pizza_app.services.invoice_service import InvoiceService
from pizza_app.services.pricing_service import PricingService
from ..domain.models import Order, OrderItem, Pizza
from ..data_access.dao import OrderDAO

class OrderService:
    def __init__(self, order_dao: OrderDAO, invoice_service: InvoiceService, pricing_service: PricingService) -> None:
        self.order_dao = order_dao
        self.invoice_service = invoice_service
        self.pricing_service = pricing_service

    def checkout(self, items: Sequence[Tuple[Pizza, int]]) -> tuple[Order, str]:
        order_items = [
            OrderItem(pizza=pizza, quantity=qty, unit_price_chf=pizza.price_chf, line_total_chf=round(pizza.price_chf * qty, 2))
            for pizza, qty in items
        ]
        subtotal, discount, total = self.pricing_service.totals_from_lines(item.line_total_chf for item in order_items)
        order = Order(subtotal_chf=subtotal, discount_chf=discount, total_chf=total, items=order_items)
        created_order = self.order_dao.create(order)
        loaded_order = self.order_dao.get_with_items(created_order.id)
        path = self.invoice_service.generate_pdf(loaded_order)
        return created_order, path

    def list_recent(self, limit: int = 200) -> List[Order]:
        return self.order_dao.list_recent(limit=limit)

    def get_with_items(self, order_id: int) -> Optional[Order]:
        return self.order_dao.get_with_items(order_id)