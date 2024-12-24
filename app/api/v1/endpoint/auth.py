from fastapi import APIRouter, HTTPException, status
from app.service import facade

route = APIRouter(prefix='/api/v1/auth', tags=['auth'])


@route.post('/login')
async def login():
    ...


@route.post('/signup')
async def signup():
    ...

