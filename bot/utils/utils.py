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