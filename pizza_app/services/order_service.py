from typing import List, Optional, Sequence
from ..domain.models import Order, OrderItem
from ..data_access.dao import OrderDAO

class OrderService:
    def __init__(self, order_dao: OrderDAO):
        self.order_dao = order_dao

    def create(self, order: Order) -> Order:
        return self.order_dao.create(order)

    def list_recent(self, limit: int = 200) -> List[Order]:
        return self.order_dao.list_recent(limit=limit)

    def get_with_items(self, order_id: int) -> Optional[Order]:
        return self.order_dao.get_with_items(order_id)