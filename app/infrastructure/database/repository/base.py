from abc import ABC
from typing import Type, TypeVar, Generic, Optional, Any, Dict, List

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    def __init__(self, session, model: Type[T]):
        self.session = session
        self.model = model

    async def commit_or_rollback(self):
        try:
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise ValueError(f"Database error: {e}") from e

    async def get_by_id(
        self, id: int, return_fields: Optional[List[str]]
    ) -> Optional[Dict[str, Any]]:
        columns = [getattr(self.model, field) for field in return_fields]
        stmt = select(*columns).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.mappings().first()
