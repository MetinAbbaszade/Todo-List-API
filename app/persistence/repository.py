from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

class IRepository(ABC):
    @abstractmethod
    def get_all(self, session: AsyncSession):
        ...
    
    @abstractmethod
    def get(self, obj_id, session: AsyncSession):
        ...

    @abstractmethod
    def add(self, obj, session: AsyncSession):
        ...

    @abstractmethod
    def update(self, obj_id, obj, session: AsyncSession):
        ...

    @abstractmethod
    def delete(self, obj_id, session: AsyncSession):
        ...