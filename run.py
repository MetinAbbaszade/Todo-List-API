from app import create_app, create_db_and_tables
import uvicorn


if __name__ == "__main__":
    app = create_app()
    create_db_and_tables()
    uvicorn.run(app, host='0.0.0.0', port=8000)