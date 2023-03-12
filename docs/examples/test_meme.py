import asyncio

from meme_generator import get_meme


async def main():
    meme = get_meme("petpet")
    result = await meme(images=["avatar.jpg"], texts=[], args={"circle": True})

    with open("result.gif", "wb") as f:
        f.write(result.getvalue())


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
