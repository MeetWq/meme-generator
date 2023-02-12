from io import BytesIO
from typing import Union
from pathlib import Path
from pil_utils import BuildImage
from argparse import ArgumentParser
from dataclasses import dataclass, field
from pydantic import BaseModel, ValidationError
from typing import List, Dict, Any, Optional, Callable, Type, TypeVar

from .exception import (
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
    default_texts: List[str] = field(default_factory=list)
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
        images: Union[List[str], List[Path], List[bytes], List[BytesIO]] = [],
        texts: List[str] = [],
        args: Optional[Union[BaseModel, Dict[str, Any]]] = None,
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
        if args:
            if isinstance(args, BaseModel):
                model = args
            elif args_type := self.params_type.args_type:
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
