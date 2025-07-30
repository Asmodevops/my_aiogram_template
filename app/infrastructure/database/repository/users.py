from typing import Optional, List, Dict, Any

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.infrastructure.database.models.users import User
from app.infrastructure.database.repository.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session):
        super().__init__(session, User)

    async def create_user(
            self, telegram_id, first_name, last_name, full_name, username
    ) -> User:
        stmt = (
            insert(User)
            .values(
                telegram_id=telegram_id,
                first_name=first_name,
                last_name=last_name,
                full_name=full_name,
                username=username,
            )
            .on_conflict_do_update(
                index_elements=["telegram_id"],
                set_={
                    "first_name": first_name,
                    "last_name": last_name,
                    "full_name": full_name,
                    "username": username,
                },
            )
            .returning(User)
        )
        result = await self.session.execute(stmt)
        await self.commit_or_rollback()
        return result.scalar_one()

    async def get_by_telegram_id(
            self,
            telegram_id: int,
            return_fields: Optional[List[str]]
    ) -> Optional[Dict[str, Any]]:
        columns = [getattr(User, field) for field in return_fields]
        stmt = select(*columns).where(User.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        return result.mappings().first()
