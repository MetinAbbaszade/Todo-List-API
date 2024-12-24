from fastapi import APIRouter, HTTPException, status, Depends
from app.service import facade
from app.api.v1.schema.auth import UserModel
from app.extensions import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from datetime import datetime

route = APIRouter(prefix='/api/v1/auth', tags=['auth'])

SECRETKEY = 'superincrediblesuperfantasticsecretmoresecretmostsecretkey'
ALGHORITM = 'HS256'



@route.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserModel)
async def signup(user: UserModel, db: AsyncSession = Depends(get_db)):
    user.id = uuid4()
    user.created_at = datetime.now()
    user.updated_at = datetime.now()

    existing_user = await facade.get_user(obj_id=user.id, db=db)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    new_user = await facade.add_user(user=user, db=db)
    return new_user



@route.post('/login')
async def login():
    ...