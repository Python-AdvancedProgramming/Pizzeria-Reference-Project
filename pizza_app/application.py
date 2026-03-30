"""NiceGUI app wiring (views + controllers).

Object-oriented entrypoint: `PizzaApplication` wires dependencies and runs NiceGUI.
"""

from __future__ import annotations

from typing import Optional

from nicegui import ui

from .data_access.db import Database
from .data_access.dao import OrderDAO, PizzaDAO
from .services.pricing import PricingService
from .services.invoice import InvoiceService
from .ui.controllers import AdminController, OrderController
from .ui.pages import Pages


class PizzaApplication:
    """Application composition root."""

    def __init__(self, database: Optional[Database] = None, invoice_dir: str = "./data/invoices") -> None:
        self.database = database or Database()
        self.invoice_dir = invoice_dir

        self.database.init_schema_and_seed()
        engine = self.database.engine

        self.pizza_dao = PizzaDAO(engine)
        self.order_dao = OrderDAO(engine)
        self.pricing = PricingService()
        self.invoice = InvoiceService(invoice_dir=self.invoice_dir)

        self.order_controller = OrderController(
            pizza_dao=self.pizza_dao,
            order_dao=self.order_dao,
            pricing=self.pricing,
            invoice=self.invoice,
        )
        self.admin_controller = AdminController(order_dao=self.order_dao)
        self.pages = Pages(order_controller=self.order_controller, admin_controller=self.admin_controller)

    def run(self, host: str = "0.0.0.0", port: int = 8080, reload: bool = False) -> None:
        """Run the NiceGUI application."""
        self.pages.register()
        ui.run(host=host, port=port, reload=reload)
