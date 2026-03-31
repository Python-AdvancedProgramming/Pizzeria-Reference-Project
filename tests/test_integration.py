from pathlib import Path

from pizza_app.data_access.dao import PizzaDAO, OrderDAO
from pizza_app.services.invoice_service import InvoiceService
from pizza_app.services.order_service import OrderService
from pizza_app.services.pizza_service import PizzaService
from pizza_app.services.pricing_service import PricingService
from pizza_app.ui.controllers import ShoppingController

def test_checkout_single_pizza_creates_order(database, seeded_db, tmp_path):
    pricing_service = PricingService()
    invoice_service = InvoiceService(invoice_dir=str(tmp_path))

    controller = ShoppingController(
        pizza_service=PizzaService(pizza_dao=PizzaDAO(database.engine)),
        order_service=OrderService(
            order_dao=OrderDAO(database.engine), 
            invoice_service=invoice_service, 
            pricing_service=pricing_service
        ),
        pricing_service=pricing_service,
        invoice_service=invoice_service,
    )

    controller.set_quantity(1, 1)
    order, invoice_path = controller.checkout()

    assert order is not None
    assert order.id is not None
    assert order.total_chf > 0
    assert Path(invoice_path).exists()


def test_checkout_multiple_pizzas_applies_discount(database, seeded_db, tmp_path):
    pricing_service = PricingService()
    invoice_service = InvoiceService(invoice_dir=str(tmp_path))
    controller = ShoppingController(
        pizza_service=PizzaService(pizza_dao=PizzaDAO(database.engine)),
        order_service=OrderService(
            order_dao=OrderDAO(database.engine),
            invoice_service=invoice_service, 
            pricing_service=pricing_service
        ),
        pricing_service=pricing_service,
        invoice_service=invoice_service,
    )

    controller.set_quantity(1, 3)  # 3 x 10 = 30
    controller.set_quantity(2, 2)  # 2 x 15 = 30
    order, invoice_path = controller.checkout()

    assert order.subtotal_chf == 60.0
    assert order.discount_chf == 6.0
    assert order.total_chf == 54.0
    assert Path(invoice_path).exists()


def test_checkout_exactly_50_does_not_apply_discount(database, seeded_db, tmp_path):
    pricing_service = PricingService()
    invoice_service = InvoiceService(invoice_dir=str(tmp_path))
    controller = ShoppingController(
        pizza_service=PizzaService(pizza_dao=PizzaDAO(database.engine)),
        order_service=OrderService(
            order_dao=OrderDAO(database.engine), 
            invoice_service=invoice_service, 
            pricing_service=pricing_service
        ),
        pricing_service=pricing_service,
        invoice_service=invoice_service,
    )

    controller.set_quantity(1, 2)  # 2 x 10 = 20
    controller.set_quantity(2, 2)  # 2 x 15 = 30
    order, invoice_path = controller.checkout()

    assert order.subtotal_chf == 50.0
    assert order.discount_chf == 0.0
    assert order.total_chf == 50.0
    assert Path(invoice_path).exists()