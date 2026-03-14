# backend

Django REST API backend for Chatodon. Handles authentication, rooms, and messages.

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv)
- PostgreSQL
- Redis

## Setup

1. Install dependencies:

```bash
uv sync
```

2. Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

3. Apply migrations:

```bash
uv run python manage.py migrate
```

## Running

```bash
uv run python manage.py runserver
```
