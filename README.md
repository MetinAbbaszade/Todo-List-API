# Todo List API

A REST API for managing todo items with user signup and JWT-based login. Each user can create, read, update and delete their own todos.

This is my solution to the [roadmap.sh Todo List API](https://roadmap.sh/projects/todo-list-api) project.

## Tech stack

- Python 3.12
- FastAPI + Uvicorn
- SQLModel (SQLAlchemy) with MySQL via PyMySQL
- PyJWT for access tokens, passlib (bcrypt) for password hashing
- Poetry for dependency management

## Project structure

```
app/
├── api/v1/
│   ├── endpoint/      # Route handlers (auth, todo)
│   └── schema/        # Pydantic request/response models, JWT helpers
├── models/            # SQLModel tables (User, ToDo)
├── persistence/       # Generic repository for database access
├── service/           # Facade that connects routes to repositories
├── extensions.py      # Database session dependency
└── __init__.py        # App factory, database engine
run.py                 # Entry point
```

## Getting started

1. Install dependencies:

   ```bash
   poetry install
   ```

2. Create a MySQL database named `Todo_List` and set the connection string in `app/__init__.py`:

   ```python
   MySQL = 'mysql+pymysql://<user>:<password>@localhost/Todo_List'
   ```

3. Run the server (tables are created on startup):

   ```bash
   poetry run python run.py
   ```

The API runs at `http://localhost:8000`. Interactive docs are at `http://localhost:8000/docs`.

## Endpoints

All routes are prefixed with `/api/v1`.

### Auth

| Method | Path           | Description                                                           |
|--------|----------------|-----------------------------------------------------------------------|
| POST   | `/auth/signup` | Register a user (JSON: `name`, `email`, `password`)                   |
| POST   | `/auth/login`  | Log in (form data: `username`, `email`, `password`), returns a JWT    |

### Todos

Send the token from login as `Authorization: Bearer <token>`.

| Method | Path          | Auth | Description                          |
|--------|---------------|------|--------------------------------------|
| GET    | `/todo/`      | No   | List all todos                       |
| GET    | `/todo/{id}`  | Yes  | Get a todo you own                   |
| POST   | `/todo/`      | Yes  | Create a todo (`title`, `description`) |
| PUT    | `/todo/{id}`  | Yes  | Update a todo you own                |
| DELETE | `/todo/{id}`  | Yes  | Delete a todo you own                |

### Example

```bash
# Sign up
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "email": "john@example.com", "password": "secret"}'

# Log in
curl -X POST http://localhost:8000/api/v1/auth/login \
  -F username=John -F email=john@example.com -F password=secret

# Create a todo
curl -X POST http://localhost:8000/api/v1/todo/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'
```

