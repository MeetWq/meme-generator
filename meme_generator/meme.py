import pkgutil
import importlib
from io import BytesIO
from typing import Union
from pathlib import Path
from pil_utils import BuildImage
from dataclasses import dataclass
from argparse import ArgumentParser
from pydantic import BaseModel, ValidationError
from typing import List, Dict, Any, Optional, Callable, Type, TypeVar

from .log import logger
from .exception import (
    NoSuchMeme,
    ImageNumberMismatch,
    TextNumberMismatch,
    ArgModelMismatch,
    OpenImageFailed,
)


MemeArgsModel = TypeVar("MemeArgsModel", bound=BaseModel)

MemeFunction = Callable[[List[BuildImage], List[str], Optional[MemeArgsModel]], BytesIO]


@dataclass
class MemeArgsType:
    parser: ArgumentParser
    model: Type[BaseModel]


@dataclass
class MemeParamsType:
    min_images: int = 0
    max_images: int = 0
    min_texts: int = 0
    max_texts: int = 0
    args_type: Optional[MemeArgsType] = None


@dataclass
class Meme:
    key: str
    keywords: List[str]
    function: MemeFunction
    params_type: MemeParamsType

    def __call__(
        self,
        *,
        images: List[Union[str, Path, bytes, BytesIO]] = [],
        texts: List[str] = [],
        args: Dict[str, Any] = {},
    ) -> BytesIO:

        if not (
            self.params_type.min_images <= len(images) <= self.params_type.max_images
        ):
            raise ImageNumberMismatch(
                self.key, self.params_type.min_images, self.params_type.max_images
            )

        if not (self.params_type.min_texts <= len(texts) <= self.params_type.max_texts):
            raise TextNumberMismatch(
                self.key, self.params_type.min_texts, self.params_type.max_texts
            )

        model = None
        if args_type := self.params_type.args_type:
            try:
                model = args_type.model.parse_obj(args)
            except ValidationError as e:
                raise ArgModelMismatch(self.key, str(e))

        imgs: List[BuildImage] = []
        try:
            for image in images:
                if isinstance(image, bytes):
                    image = BytesIO(image)
                imgs.append(BuildImage.open(image))
        except Exception as e:
            raise OpenImageFailed(self.key, str(e))

        return self.function(imgs, texts, model)


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
    args_type: Optional[MemeArgsType] = None,
):
    if key in _memes:
        logger.warning(f"Meme with key {key} always exists!")
        return

    _memes[key] = Meme(
        key,
        keywords,
        function,
        MemeParamsType(min_images, max_images, min_texts, max_texts, args_type),
    )


def get_meme(key: str) -> Meme:
    if key not in _memes:
        raise NoSuchMeme(key)
    return _memes[key]


def get_meme_keys() -> List[str]:
    return list(_memes.keys())


load_memes(Path(__file__).parent / "memes")
