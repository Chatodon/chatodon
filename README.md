# Chatodon

Just a simple self-hosted chat.

This work is licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
https://creativecommons.org/licenses/by-nc/4.0/

## Deployment

### Prerequisites

- Docker with Compose plugin

### Setup

```bash
cp .env.example .env
```

Edit `.env` and set at minimum:

| Variable | Description |
|---|---|
| `DOMAIN` | Your domain name |
| `DJANGO_SECRET_KEY` | Random secret string |
| `JWT_SECRET_KEY` | Random secret string |
| `POSTGRES_PASSWORD` | Database password |
| `TRAEFIK_HOST` | Interface to bind (`0.0.0.0` for all, `127.0.0.1` for localhost only) |

### Run (HTTP)

```bash
docker compose up -d
```

### Run (HTTPS with Let's Encrypt)

Set `ACME_EMAIL` in `.env`, then:

```bash
docker compose -f docker-compose.yml -f docker-compose.ssl.yml up -d
```

Traefik will automatically obtain and renew a TLS certificate for `DOMAIN`.
HTTP traffic is redirected to HTTPS.

### Django admin

Create a superuser after the first start:

```bash
docker compose exec backend uv run python manage.py createsuperuser
```

Admin panel is available at `https://<DOMAIN>/admin/`.
