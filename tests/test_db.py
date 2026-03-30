from sqlmodel import select

from pizza_app.domain.models import Pizza, Order, OrderItem


def test_menu_query_returns_seeded_pizzas(seeded_db):
    pizzas = seeded_db.exec(select(Pizza)).all()

    assert len(pizzas) == 2
    assert pizzas[0].name == "Margherita"


def test_saving_order_persists_order_and_items(db, seeded_db):
    order = Order(subtotal_chf=20.0, discount_chf=0.0, total_chf=20.0)
    db.add(order)
    db.commit()
    db.refresh(order)

    item = OrderItem(
        order_id=order.id,
        pizza_id=1,
        quantity=2,
        unit_price_chf=10.0,
        line_total_chf=20.0,
    )
    db.add(item)
    db.commit()

    items = db.exec(
        select(OrderItem).where(OrderItem.order_id == order.id)
    ).all()

    assert len(items) == 1