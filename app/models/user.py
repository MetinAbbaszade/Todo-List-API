from app.models.basemodel import BaseModel
from sqlmodel import Field, String
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel, table=True):
    name: str = Field(String[100])
    email: str = Field(String[100])
    password: str = Field(String[100])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'password' in kwargs:
            self.password = self.hash_password(kwargs['password'])

    
    def to_dict(self):
        dictionary = super().to_dict()
        dictionary.update({
            "name": self.name,
            "email": self.email,
            "password": self.password
        })

        return dictionary

    @staticmethod
    def hash_password(password):
        return pwd_context.hash(password)
    

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)