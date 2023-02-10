from io import BytesIO
from pydantic import BaseModel
from pil_utils import BuildImage
from dataclasses import dataclass
from argparse import ArgumentParser
from typing import List, Optional, Callable, Type, TypeVar


MemeArgsModel = TypeVar("MemeArgsModel", bound=BaseModel)

MemeFunction = Callable[[List[BuildImage], List[str], MemeArgsModel], BytesIO]


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

    def __hash__(self) -> int:
        return hash(self.key)
