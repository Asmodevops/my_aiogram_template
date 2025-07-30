from pydantic import ValidationError

from app.bot.schemas import UserSchema


class UserServices:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    async def get_validated_user_by_telegram_id(self, telegram_id: int):
        raw_user = await self.user_repo.get_by_telegram_id(
            telegram_id=telegram_id, return_fields=["telegram_id", "full_name", "username"]
        )

        if not raw_user:
            return None

        try:
            user = UserSchema.model_validate(raw_user)
            return user
        except ValidationError:
            return None
