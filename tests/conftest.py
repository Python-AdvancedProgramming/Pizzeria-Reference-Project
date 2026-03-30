import pytest
from sqlmodel import Session, SQLModel

from pizza_app.domain.models import Pizza
from pizza_app.data_access.db import Database


@pytest.fixture(scope="function")
def database():
    db = Database("sqlite:///:memory:")
    SQLModel.metadata.create_all(db.engine)
    yield db
    SQLModel.metadata.drop_all(db.engine)


@pytest.fixture(scope="function")
def db(database):
    with Session(database.engine) as session:
        yield session


@pytest.fixture
def seeded_db(db):
    pizzas = [
        Pizza(name="Margherita", price_chf=10.0, ingredients="tomato, mozzarella"),
        Pizza(name="Salami", price_chf=15.0, ingredients="tomato, mozzarella, salami"),
    ]
    db.add_all(pizzas)
    db.commit()
    for pizza in pizzas:
        db.refresh(pizza)
    return db


@pytest.fixture
def sample_items():
    return [20.0, 15.0]