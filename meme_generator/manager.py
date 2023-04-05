import importlib
import importlib.util
import pkgutil
from pathlib import Path
from typing import Dict, List, Optional, Union

from .config import meme_config
from .exception import NoSuchMeme
from .log import logger
from .meme import Meme, MemeArgsType, MemeFunction, MemeParamsType

_memes: Dict[str, Meme] = {}


def path_to_module_name(path: Path) -> str:
    rel_path = path.resolve().relative_to(Path.cwd().resolve())
    if rel_path.stem == "__init__":
        return ".".join(rel_path.parts[:-1])
    else:
        return ".".join(rel_path.parts[:-1] + (rel_path.stem,))


def load_meme(module_path: Union[str, Path]):
    module_name = (
        path_to_module_name(module_path)
        if isinstance(module_path, Path)
        else module_path
    )
    try:
        importlib.import_module(module_name)
    except Exception as e:
        logger.opt(colors=True, exception=e).error(f"Failed to import {module_path}!")


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
        if not (module_loader := module_spec.loader):
            continue
        try:
            module = importlib.util.module_from_spec(module_spec)
            module_loader.exec_module(module)
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                f"Failed to import {module_path}!"
            )


def add_meme(
    key: str,
    function: MemeFunction,
    *,
    min_images: int = 0,
    max_images: int = 0,
    min_texts: int = 0,
    max_texts: int = 0,
    default_texts: List[str] = [],
    args_type: Optional[MemeArgsType] = None,
    keywords: List[str] = [],
    patterns: List[str] = [],
):
    if key in _memes:
        logger.warning(f'Meme with key "{key}" already exists!')
        return

    if key in meme_config.meme.meme_disabled_list:
        logger.warning(f'The key "{key}" is in the disabled list!')
        return

    meme = Meme(
        key,
        function,
        MemeParamsType(
            min_images, max_images, min_texts, max_texts, default_texts, args_type
        ),
        keywords=keywords,
        patterns=patterns,
    )

    _memes[key] = meme


def get_meme(key: str) -> Meme:
    if key not in _memes:
        raise NoSuchMeme(key)
    return _memes[key]


def get_memes() -> List[Meme]:
    return list(_memes.values())


def get_meme_keys() -> List[str]:
    return list(_memes.keys())
