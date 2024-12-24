from app.persistence.repository import MemoryRepository
from app.models.user import User
from app.models.todo import ToDo
from sqlalchemy.ext.asyncio import AsyncSession

class HBNBFacade:
    def __init__(self):
        self.user_repo = MemoryRepository(User)
        self.todo_repo = MemoryRepository(ToDo)

    async def add_user(self, user, db: AsyncSession):
        new_user_data = user.dict()
        new_user = User(**new_user_data)
        await self.user_repo.add(obj=new_user, session=db)
        return new_user

    async def get_user(self, obj_id, db: AsyncSession):
        return await self.user_repo.get(obj_id=obj_id, session=db)
    
    async def get_all_users(self, db: AsyncSession):
        return await self.user_repo.get_all(session=db)
    
    async def add_todo_list(self, todo, db: AsyncSession):
        new_todo_list_data = todo.dict()
        new_todo_list = ToDo(**new_todo_list_data)
        await self.todo_repo.add(obj=new_todo_list, session=db)
        return new_todo_list

    async def get_todo_list(self, todo_id, db: AsyncSession):
        return await self.todo_repo.get(obj_id=todo_id, session=db)
    
    async def get_all_todo_lists(self, db: AsyncSession):
        return await self.todo_repo.get_all(session=db)

    async def update_todo_list(self, todo_id, new_todo, db: AsyncSession):
        new_todo_list_data = new_todo.dict()
        new_todo_list = ToDo(**new_todo_list_data)
        await self.todo_repo.update(obj_id=todo_id, obj=new_todo_list, session=db)
        return new_todo_list

    async def delete_todo_list(self, todo_id, db: AsyncSession):
        return await self.todo_repo.delete(obj_id=todo_id, session=db)   