from pydantic import BaseModel


class UserSchema(BaseModel):
    telegram_id: int
    full_name: str
    username: str
