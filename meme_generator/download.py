import asyncio
import hashlib
import json
from pathlib import Path
from typing import List, Tuple

import httpx
import tqdm

from .config import meme_config
from .log import logger
from .version import __version__


def _resource_url(path: str) -> str:
    return f"{meme_config.resource.resource_url}/v{__version__}/{path}"


async def check_resources():
    semaphore = asyncio.Semaphore(10)

    async def _download(client: httpx.AsyncClient, url: str):
        async with semaphore:
            try:
                resp = await client.get(url, timeout=20, follow_redirects=True)
                resp.raise_for_status()
                return resp.content
            except httpx.HTTPError as e:
                logger.warning(f"{url} download failed！\n{e}")

    async with httpx.AsyncClient() as client:
        if content := await _download(
            client, _resource_url("resources/resource_list.json")
        ):
            resource_list = json.loads(content.decode("utf-8"))
        else:
            logger.warning("resource_list.json download failed！")
            return

    download_list: List[Tuple[Path, str]] = []
    for resource in resource_list:
        file_name = str(resource["path"])
        file_hash = str(resource["hash"])
        file_path = Path(__file__).parent / "memes" / file_name
        if (
            file_path.exists()
            and hashlib.md5(file_path.read_bytes()).hexdigest() == file_hash
        ):
            continue
        else:
            download_list.append(
                (file_path, _resource_url(f"meme_generator/memes/{file_name}"))
            )

    if len(download_list):
        logger.info("Downloading images ...")
    else:
        return

    async with httpx.AsyncClient() as client:

        async def download_image(file_path: Path, url: str):
            if content := await _download(client, url):
                file_path.parent.mkdir(parents=True, exist_ok=True)
                with file_path.open("wb") as f:
                    f.write(content)

        pbar = tqdm.tqdm(total=len(download_list))
        tasks = [download_image(file_path, url) for file_path, url in download_list]
        for task in asyncio.as_completed(tasks):
            await task
            pbar.update()
