from fastapi import APIRouter, HTTPException, status
from app.service import facade
from app.api.v1.schema.todo import ToDoModel

route = APIRouter(prefix='/api/v1/todo', tags=['todo'])

@route.get('/')
async def get_todo_lists():
    ...

@route.get('/{todo_id}')
async def get_todo_lists(todo_id):
    ...

@route.post('/')
async def create_todo_list():
    ...

@route.put('/{todo_id}')
async def update_todo_list():
    ...

@route.delete('/{todo_id}')
async def delete_todo_list():
    ...