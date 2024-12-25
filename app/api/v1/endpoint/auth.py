from fastapi import APIRouter, HTTPException, status, Depends
from app.service import facade
from app.api.v1.schema.auth import UserModel
from app.extensions import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from datetime import datetime
from app.api.v1.schema.auth import create_access_token
from app.api.v1.schema.auth import CustomOauth2PasswordRequestForm
from app.models.user import User

route = APIRouter(prefix='/api/v1/auth', tags=['auth'])




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


@route.post('/login', response_model=dict, status_code=status.HTTP_201_CREATED)
async def login(formdata: CustomOauth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    email = formdata.email
    user: User = await facade.get_user_by_email(email=email, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found!'
        )
    password = formdata.password
    if not user.verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='False password'
        )
    payload = {
        "sub": user.id,
        "username": user.name,
        "email": user.email
    }
    access_token = await create_access_token(payload)
    return {"access_token": access_token}