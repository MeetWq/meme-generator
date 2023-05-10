import asyncio
import hashlib
import json
import time
from pathlib import Path
from typing import List, Tuple

import httpx
from rich.progress import Progress

from .config import meme_config
from .log import logger
from .version import __version__


def _resource_url(base_url: str, name: str) -> str:
    return f"{base_url}v{__version__}/{name}"


# https://github.com/mnixry/nonebot-plugin-gocqhttp/blob/main/nonebot_plugin_gocqhttp/process/download.py
async def get_fastest_mirror() -> List[str]:
    assert meme_config.resource.resource_urls, "No resource url specified."

    async def head_mirror(client: httpx.AsyncClient, base_url: str):
        begin_time = time.time()
        response = await client.head(
            _resource_url(base_url, "resources/fonts/NotoSansSC-Regular.otf"), timeout=5
        )
        response.raise_for_status()
        elapsed_time = (time.time() - begin_time) * 1000
        return {"base_url": base_url, "elapsed_time": elapsed_time}

    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            *(
                head_mirror(client, domain)
                for domain in meme_config.resource.resource_urls
            ),
            return_exceptions=True,
        )
    results = sorted(
        (result for result in results if not isinstance(result, Exception)),
        key=lambda r: r["elapsed_time"],
    )
    return [result["base_url"] for result in results]


async def check_resources():
    semaphore = asyncio.Semaphore(10)

    available_urls = (
        [meme_config.resource.resource_url]
        if meme_config.resource.resource_url
        else (await get_fastest_mirror())
    )
    logger.debug(f"Available resource urls: {available_urls}")
    if not available_urls:
        logger.warning("No resource url available.")
        return

    async def _download(client: httpx.AsyncClient, name: str):
        async with semaphore:
            for base_url in available_urls:
                url = _resource_url(base_url, name)
                try:
                    resp = await client.get(url, timeout=20, follow_redirects=True)
                    resp.raise_for_status()
                    return resp.content
                except httpx.HTTPError:
                    pass
            logger.warning(f"{name} download failed！")

    async with httpx.AsyncClient() as client:
        if content := await _download(client, "resources/resource_list.json"):
            resource_list = json.loads(content.decode("utf-8"))
        else:
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
            download_list.append((file_path, f"meme_generator/memes/{file_name}"))

    if len(download_list):
        logger.info("Downloading images ...")
    else:
        return

    async with httpx.AsyncClient() as client:

        async def download_image(file_path: Path, file_name: str):
            if content := await _download(client, file_name):
                file_path.parent.mkdir(parents=True, exist_ok=True)
                with file_path.open("wb") as f:
                    f.write(content)

        with Progress(
            *Progress.get_default_columns(), "[yellow]{task.completed}/{task.total}"
        ) as progress:
            progress_task = progress.add_task(
                "[green]Downloading...", total=len(download_list)
            )
            tasks = [
                download_image(file_path, file_name)
                for file_path, file_name in download_list
            ]
            for task in asyncio.as_completed(tasks):
                await task
                progress.update(progress_task, advance=1)
