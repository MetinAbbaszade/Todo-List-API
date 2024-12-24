from app.models.basemodel import BaseModel
from sqlmodel import Field, String

class ToDo(BaseModel, table=True):
    title: str = Field(String[100])
    description: str = Field(String[100])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }