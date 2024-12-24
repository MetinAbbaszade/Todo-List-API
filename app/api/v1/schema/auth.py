from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class UserModel(BaseModel):
    id: UUID | None = None
    name: str
    email: str
    password: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

async def create_access_token():
    ...

async def decode_token():
    ...