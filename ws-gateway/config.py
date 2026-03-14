import os

from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

DJANGO_AUTH_URL = os.getenv("DJANGO_AUTH_URL", "http://localhost:8001/account/me/")
DJANGO_MY_ROOM_URL = os.getenv("DJANGO_MY_ROOM_URL", "http://localhost:8001/rooms/my/")
