import httpx

from config import DJANGO_AUTH_URL, DJANGO_MY_ROOM_URL


async def get_user_from_session(sessionid: str):
    cookies = {"sessionid": sessionid}
    async with httpx.AsyncClient(cookies=cookies) as client:
        r = await client.get(DJANGO_AUTH_URL)
        if r.status_code != 200:
            return None
        return r.json()


async def get_user_rooms(sessionid: str):
    cookies = {"sessionid": sessionid}
    async with httpx.AsyncClient(cookies=cookies) as client:
        r = await client.get(DJANGO_MY_ROOM_URL)
        if r.status_code != 200:
            return []
        data = r.json().get("results", [])
        return [room["id"] for room in data]
