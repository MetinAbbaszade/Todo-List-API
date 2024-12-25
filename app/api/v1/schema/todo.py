from pydantic import BaseModel
from uuid import UUID, uuid4

class ToDoModel(BaseModel):
    id: UUID | None = None
    title: str
    description: str
    owner_id: UUID | None = None
