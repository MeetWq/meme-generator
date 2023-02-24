import json
import httpx
import asyncio
import hashlib
from pathlib import Path

from .log import logger
from .config import meme_config
from .version import __version__


async def _download_url(url: str) -> bytes:
    async with httpx.AsyncClient() as client:
        for i in range(3):
            try:
                resp = await client.get(url, timeout=20)
                resp.raise_for_status()
                return resp.content
            except httpx.HTTPError:
                logger.debug(f"Error downloading {url}, retry {i}/3")
                await asyncio.sleep(3)
    raise Exception(f"{url} download failed！")


async def _download_resource(path: str) -> bytes:
    return await _download_url(
        f"{meme_config.resource.resource_url}/blob/v{__version__}/{path}"
    )


async def _download_image(file_name: str, file_hash: str):
    file_path = Path(__file__).parent / "memes" / file_name
    if (
        file_path.exists()
        and hashlib.md5(file_path.read_bytes()).hexdigest() == file_hash
    ):
        return
    logger.debug(f"Downloading {file_name} ...")
    try:
        content = await _download_resource(f"meme_generator/memes/{file_name}")
        with file_path.open("wb") as f:
            f.write(content)
    except Exception as e:
        logger.warning(str(e))


async def check_resources():
    resource_list = json.loads(
        (await _download_resource("resources/resource_list.json")).decode("utf-8")
    )
    tasks = []
    for resource in resource_list:
        file_name = str(resource["path"])
        file_hash = str(resource["hash"])
        tasks.append(_download_image(file_name, file_hash))
    await asyncio.gather(*tasks)
