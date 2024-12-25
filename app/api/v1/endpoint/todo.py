from app.service import facade
from app.api.v1.schema.todo import ToDoModel
from app.api.v1.schema.auth import get_current_user
from app.models.user import User
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.extensions import get_db
from uuid import uuid4, UUID
from typing import List
from app.models.todo import ToDo


route = APIRouter(prefix='/api/v1/todo', tags=['todo'])


@route.get('/', response_model=List[ToDoModel], status_code=status.HTTP_200_OK)
async def get_all_todo_lists(
    db: AsyncSession = Depends(get_db)
    ):
    todo_lists: List[ToDo] = await facade.get_all_todo_lists(db=db)

    data = []
    for todo_list in todo_lists:
        data.append(todo_list.to_dict())

    return data


@route.get('/{todo_id}', response_model=ToDoModel, status_code=status.HTTP_200_OK)
async def get_todo_list(
    todo_id: UUID, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    
    todo: ToDo = await facade.get_todo_list(todo_id=todo_id, db=db)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User not found'
        )
    
    if todo.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized'
        )
    
    return todo

@route.post('/', response_model=ToDoModel, status_code=status.HTTP_201_CREATED)
async def create_todo_list(
    todo: ToDoModel, 
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
    ):
    todo.id = uuid4()
    todo.owner_id = current_user.id

    new_user = await facade.add_todo_list(todo=todo, db=db)
    return new_user

@route.put('/{todo_id}', status_code=status.HTTP_200_OK)
async def update_todo_list(
    todo_id: UUID, 
    todo: ToDoModel, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    existing_todo: ToDo = await facade.get_todo_list(todo_id=todo_id, db=db)
    if not existing_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Todo List Not found'
        )
    
    todo.id = existing_todo.id
    todo.owner_id = existing_todo.owner_id

    if todo.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized'
        )

    new_todo = await facade.update_todo_list(todo_id=todo_id, new_todo=todo, db=db)
    return new_todo

@route.delete('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_list(
    todo_id: UUID, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    todo: ToDo = await facade.get_todo_list(todo_id, db=db)
    
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    if todo.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized'
        )
    await facade.delete_todo_list(todo_id, db=db)
    return None  