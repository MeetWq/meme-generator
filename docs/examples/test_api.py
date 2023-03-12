import asyncio
import json

import httpx


async def main():
    files = [("images", open("avatar.jpg", "rb"))]
    texts = []
    args = {"circle": True}
    data = {"texts": texts, "args": json.dumps(args)}

    url = "http://127.0.0.1:2233/memes/petpet/"
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, files=files, data=data)

    with open("result.gif", "wb") as f:
        f.write(resp.content)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
