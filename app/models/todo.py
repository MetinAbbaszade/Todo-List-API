from app.models.basemodel import BaseModel
from sqlmodel import Field, String
from uuid import UUID

class ToDo(BaseModel, table=True):
    title: str = Field(String[100])
    description: str = Field(String[100])
    owner_id: UUID = Field(primary_key=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "owner_id": self.owner_id
        }