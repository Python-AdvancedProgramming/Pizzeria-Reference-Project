"""Database configuration and initialization (SQLite + SQLModel).

This module is intentionally object-oriented: it exposes a `Database` facade that
owns the SQLAlchemy engine and provides initialization + session management.
Design pattern: Implementing the object-oriented database facade
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

from sqlalchemy.engine import Engine
from sqlmodel import SQLModel, Session, create_engine

from sqlmodel import select

from ..domain.models import Pizza
from ..data_access.seed import MenuSeeder


class Database:
    """Database facade (engine + schema init + session scope)."""

    def __init__(self, database_url: Optional[str] = None, *, echo: bool = False) -> None:
        self._database_url = database_url or os.getenv("DATABASE_URL") or self._default_sqlite_url()
        # check_same_thread=False needed because NiceGUI uses threads
        self._engine: Engine = create_engine(
            self._database_url, echo=echo, connect_args={"check_same_thread": False}
        )

    @staticmethod
    def _default_sqlite_url() -> str:
        # path relative to *project root*
        Path("data").mkdir(parents=True, exist_ok=True)
        return "sqlite:///data/pizza_app.db"

    @property
    def engine(self) -> Engine:
        return self._engine

    def init_schema_and_seed(self) -> None:
        """Create tables and seed menu data if the Pizza table is empty."""
        SQLModel.metadata.create_all(self._engine)
        with Session(self._engine) as session:
            if session.exec(select(Pizza)).first() is None:
                MenuSeeder().seed(session)
                session.commit()

    @contextmanager
    def session_scope(self) -> Iterator[Session]:
        """Provide a transactional scope around a series of operations."""
        session = Session(self._engine)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
