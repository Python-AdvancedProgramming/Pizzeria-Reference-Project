
from typing import List, Optional
from ..domain.models import Pizza
from ..data_access.dao import PizzaDAO

class PizzaService:
    def __init__(self, pizza_dao: PizzaDAO):
        self.pizza_dao = pizza_dao

    def list_menu(self) -> List[Pizza]:
        return self.pizza_dao.list_menu()

    def get_by_id(self, pizza_id: int) -> Optional[Pizza]:
        return self.pizza_dao.get_by_id(pizza_id)
