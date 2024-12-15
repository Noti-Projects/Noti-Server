# Noti Server

Backend server for the Noti notification system.

## Setup

1. Install Poetry (if not already installed):
```bash
pip install poetry
```

2. Install dependencies:
```bash
poetry install
```

3. Run the server:
```bash
poetry run uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, you can access:
- API documentation: http://localhost:8000/docs
- Alternative API documentation: http://localhost:8000/redoc

## Project Structure

```
noti-server/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   ├── core/
│   │   └── config.py
│   ├── db/
│   │   └── session.py
│   ├── models/
│   │   └── message.py
│   ├── schemas/
│   │   └── message.py
│   └── main.py
├── tests/
├── alembic/
├── alembic.ini
└── pyproject.toml
```
