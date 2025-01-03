from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlmodel import SQLModel
from app.api.v1.endpoint.auth import route as auth_ns
from app.api.v1.endpoint.todo import route as todo_ns

app = FastAPI(
    title="My API",
    description="API that requires a Bearer token",
    version="1.0",
    openapi_security=[{
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }]
)
MySQL = 'mysql+pymysql://root:M3tin190534@localhost/Todo_List'

engine = create_engine(MySQL, echo=True)

def create_app():

    app.include_router(auth_ns)
    app.include_router(todo_ns)

    return app

def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)