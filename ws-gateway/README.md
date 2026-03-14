# ws-gateway

WebSocket gateway for Chatodon. Authenticates clients via session cookies, subscribes them to their chat rooms, and broadcasts real-time messages from Redis.

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv)
- Redis instance
- Running Chatodon backend (Django)

## Setup

1. Install dependencies:

```bash
uv sync
```

2. Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

## Running

```bash
uv run fastapi dev
```
