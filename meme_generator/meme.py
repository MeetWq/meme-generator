from io import BytesIO
from typing import Union
from pathlib import Path
from pil_utils import BuildImage
from argparse import ArgumentParser
from dataclasses import dataclass, field
from pydantic import BaseModel, ValidationError
from typing import (
    List,
    Dict,
    Any,
    cast,
    Literal,
    Optional,
    Callable,
    Type,
    TypeVar,
    Awaitable,
)

from .utils import run_sync, is_coroutine_callable, random_text, random_image
from .exception import (
    ImageNumberMismatch,
    TextNumberMismatch,
    ArgModelMismatch,
    OpenImageFailed,
    TextOrNameNotEnough,
)


class UserInfo(BaseModel):
    name: str = ""
    gender: Literal["male", "female", "unknown"] = "unknown"


class MemeArgsModel(BaseModel):
    user_infos: List[UserInfo] = []


ArgsModel = TypeVar("ArgsModel", bound=MemeArgsModel)

MemeFunction = Union[
    Callable[[List[BuildImage], List[str], ArgsModel], BytesIO],
    Callable[[List[BuildImage], List[str], ArgsModel], Awaitable[BytesIO]],
]


@dataclass
class MemeArgsType:
    parser: ArgumentParser
    model: Type[MemeArgsModel]


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
    function: MemeFunction
    params_type: MemeParamsType
    keywords: List[str] = field(default_factory=list)
    patterns: List[str] = field(default_factory=list)

    async def __call__(
        self,
        *,
        images: Union[List[str], List[Path], List[bytes], List[BytesIO]] = [],
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

        if args_type := self.params_type.args_type:
            args_model = args_type.model
        else:
            args_model = MemeArgsModel

        try:
            model = args_model.parse_obj(args)
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

        values = {"images": imgs, "texts": texts, "args": model}

        if is_coroutine_callable(self.function):
            return await cast(Callable[..., Awaitable[BytesIO]], self.function)(
                **values
            )
        else:
            return await run_sync(cast(Callable[..., BytesIO], self.function))(**values)

    async def generate_preview(self) -> BytesIO:
        default_images = [random_image() for _ in range(self.params_type.min_images)]
        default_texts = (
            self.params_type.default_texts
            if (
                self.params_type.min_texts
                <= len(self.params_type.default_texts)
                <= self.params_type.max_texts
            )
            else [random_text() for _ in range(self.params_type.min_texts)]
        )

        async def _generate_preview(images: List[BytesIO], texts: List[str]):
            try:
                return await self.__call__(images=images, texts=texts)
            except TextOrNameNotEnough:
                texts.append(random_text())
                return await _generate_preview(images, texts)

        return await _generate_preview(default_images, default_texts)
