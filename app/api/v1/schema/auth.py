from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from fastapi import Form, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer
import jwt
from app.models.user import User
from app.service import facade
from app.extensions import get_db

http_token = HTTPBearer()

SECRETKEY = 'superincrediblesuperfantasticsecretmoresecretmostsecretkey'
ALGHORITM = 'HS256'

class UserModel(BaseModel):
    id: UUID | None = None
    name: str
    email: str
    password: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

class CustomOauth2PasswordRequestForm:
    def __init__(
            self,
            username: str = Form(...),
            password: str = Form(...),
            email: str = Form(...)
    ):
        self.username = username
        self.password = password
        self.email = email

async def create_access_token(payload) -> str:
    data = payload.copy()
    for key, value in data.items():
        if isinstance(value, UUID):
            data[key] = str(value)

    access_token = jwt.encode(
        payload=data,
        key=SECRETKEY,
        algorithm=ALGHORITM
    )
    return access_token

async def decode_token(token):
    decoded_token = jwt.decode(
        token,
        key=SECRETKEY,
        algorithms=[ALGHORITM]
    )

    return decoded_token

async def get_token_from_header(token: str = Depends(http_token)) -> str:
    return token.credentials


async def get_current_user(token: str = Depends(get_token_from_header), db=Depends(get_db)):
    decoded_token = await decode_token(token=token)
    email: str = decoded_token.get('email')
    user: User = await facade.get_user_by_email(email=email, db=db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return user