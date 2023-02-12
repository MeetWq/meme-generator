import pkgutil
import importlib
from typing import Union
from pathlib import Path
from typing import List, Dict, Optional

from .log import logger
from .app import register_router
from .exception import NoSuchMeme
from .meme import Meme, MemeFunction, MemeArgsType, MemeParamsType


_memes: Dict[str, Meme] = dict()


def path_to_module_name(path: Path) -> str:
    rel_path = path.resolve().relative_to(Path(".").resolve())
    if rel_path.stem == "__init__":
        return ".".join(rel_path.parts[:-1])
    else:
        return ".".join(rel_path.parts[:-1] + (rel_path.stem,))


def load_memes(dir_path: Union[str, Path]):
    if isinstance(dir_path, Path):
        dir_path = str(dir_path.resolve())

    for module_info in pkgutil.iter_modules([dir_path]):
        if module_info.name.startswith("_"):
            continue
        if not (
            module_spec := module_info.module_finder.find_spec(module_info.name, None)
        ):
            continue
        if not (module_path := module_spec.origin):
            continue
        module_path = Path(module_path).resolve()
        module_name = path_to_module_name(module_path)
        try:
            importlib.import_module(module_name)
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                f"Failed to import {module_path}!"
            )


def add_meme(
    key: str,
    keywords: List[str],
    function: MemeFunction,
    *,
    min_images: int = 0,
    max_images: int = 0,
    min_texts: int = 0,
    max_texts: int = 0,
    default_texts: List[str] = [],
    args_type: Optional[MemeArgsType] = None,
):
    if key in _memes:
        logger.warning(f"Meme with key {key} always exists!")
        return

    meme = Meme(
        key,
        keywords,
        function,
        MemeParamsType(
            min_images, max_images, min_texts, max_texts, default_texts, args_type
        ),
    )

    _memes[key] = meme

    register_router(meme)


def get_meme(key: str) -> Meme:
    if key not in _memes:
        raise NoSuchMeme(key)
    return _memes[key]


def get_meme_keys() -> List[str]:
    return list(_memes.keys())
