from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class BaseModel(SQLModel):
    id: UUID = Field(default_factory=uuid4())
    created_at: datetime = Field(default_factory=datetime.now())
    updated_at: datetime = Field(default_factory=datetime.now())

    def update(self, data: dict):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_by = datetime.now()

    def to_dict(self) -> dict:
        return {
            "id": self.id
        }