import json

import httpx


async def identify_myself() -> str:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://ipapi.co/json/")
            location = json.loads(response.text)
            return (
                f'IP: {location["ip"]}, '
                f'Location: {location["city"]}, '
                f'{location["country_name"]}'
            )
    except:
        return "Unknown IP"


async def format_user_name(user) -> str:
    if user.first_name and user.last_name:
        return f"{user.first_name} {user.last_name}"
    if user.first_name:
        return user.first_name
    if user.username:
        return f"@{user.username}"
    return str(user.id)
