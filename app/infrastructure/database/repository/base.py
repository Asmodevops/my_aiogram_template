from abc import ABC
from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    def __init__(self, session, model: type[T]):
        self.session = session
        self.model = model

    async def commit_or_rollback(self):
        try:
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise ValueError(f"Database error: {e}") from e

    async def get_by_id(
        self, id: int, return_fields: list[str] | None
    ) -> dict[str, Any] | None:
        columns = [getattr(self.model, field) for field in return_fields]
        stmt = select(*columns).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.mappings().first()
