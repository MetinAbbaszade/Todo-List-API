from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from uuid import UUID

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

class MemoryRepository(IRepository):
    def __init__(self, model):
        self.model = model

    async def get_all(self, session: AsyncSession):
        return session.execute(select(self.model)).scalars().all()
    
    async def get(self, obj_id, session: AsyncSession):
        try:
            if isinstance(obj_id, str):
                obj_id = UUID(obj_id)
            else:
                pass
        except:
            raise ValueError('Value is not suitable for uuid')
        
        return session.execute(select(self.model).where(self.model.id == obj_id)).scalars().first()
    

    async def add(self, obj, session: AsyncSession):
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    async def update(self, obj_id, obj, session: AsyncSession):
        object = await self.get(obj_id=obj_id, session=session)
        obj_data = obj.dict(exclude_unset=True)
        for key, value in obj_data.items():
            setattr(object, key, value)

        session.commit()
        session.refresh(object)
        return object

    async def delete(self, obj_id, session: AsyncSession):
        object = await self.get(obj_id=obj_id, session=session)
        session.delete(object)
        session.commit()

        return object
    