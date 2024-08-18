from dataclasses import dataclass, field
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any, Literal, Optional, Protocol, TypeVar, Union

from arclet.alconna import ArgFlag, Args, Empty, Option
from arclet.alconna.action import Action
from pil_utils import BuildImage
from pydantic import BaseModel, ValidationError

from .compat import type_validate_python
from .exception import (
    ArgModelMismatch,
    ImageNumberMismatch,
    OpenImageFailed,
    TextNumberMismatch,
    TextOrNameNotEnough,
)
from .utils import random_image, random_text


class UserInfo(BaseModel):
    name: str = ""
    gender: Literal["male", "female", "unknown"] = "unknown"


class MemeArgsModel(BaseModel):
    user_infos: list[UserInfo] = []


ArgsModel = TypeVar("ArgsModel", bound=MemeArgsModel)


class MemeFunction(Protocol):
    def __call__(
        self,
        images: list[BuildImage],
        texts: list[str],
        args: ArgsModel,  # type: ignore
    ) -> BytesIO: ...


class ParserArg(BaseModel):
    name: str
    value: str
    default: Optional[Any] = None
    flags: Optional[list[ArgFlag]] = None


class ParserOption(BaseModel):
    names: list[str]
    args: Optional[list[ParserArg]] = None
    dest: Optional[str] = None
    default: Optional[Any] = None
    action: Optional[Action] = None
    help_text: Optional[str] = None
    compact: bool = False

    def option(self) -> Option:
        args = Args()
        for arg in self.args or []:
            args.add(
                name=arg.name,
                value=arg.value,
                default=arg.default or Empty,
                flags=arg.flags,
            )

        return Option(
            name="|".join(self.names),
            args=args,
            dest=self.dest,
            default=self.default or Empty,
            action=self.action,
            help_text=self.help_text,
            compact=self.compact,
        )


class CommandShortcut(BaseModel):
    key: str
    args: Optional[list[str]] = None
    humanized: Optional[str] = None


@dataclass
class MemeArgsType:
    args_model: type[MemeArgsModel]
    args_examples: list[MemeArgsModel] = field(default_factory=list)
    parser_options: list[ParserOption] = field(default_factory=list)


@dataclass
class MemeParamsType:
    min_images: int = 0
    max_images: int = 0
    min_texts: int = 0
    max_texts: int = 0
    default_texts: list[str] = field(default_factory=list)
    args_type: Optional[MemeArgsType] = None


@dataclass
class Meme:
    key: str
    function: MemeFunction
    params_type: MemeParamsType
    keywords: list[str] = field(default_factory=list)
    shortcuts: list[CommandShortcut] = field(default_factory=list)
    tags: set[str] = field(default_factory=set)
    date_created: datetime = datetime(2021, 5, 4)
    date_modified: datetime = datetime.now()

    def __call__(
        self,
        *,
        images: Union[list[str], list[Path], list[bytes], list[BytesIO]] = [],
        texts: list[str] = [],
        args: dict[str, Any] = {},
    ) -> BytesIO:
        if not (
            self.params_type.min_images <= len(images) <= self.params_type.max_images
        ):
            raise ImageNumberMismatch(
                self.params_type.min_images, self.params_type.max_images
            )

        if not (self.params_type.min_texts <= len(texts) <= self.params_type.max_texts):
            raise TextNumberMismatch(
                self.params_type.min_texts, self.params_type.max_texts
            )

        if args_type := self.params_type.args_type:
            args_model = args_type.args_model
        else:
            args_model = MemeArgsModel

        try:
            model = type_validate_python(args_model, args)
        except ValidationError as e:
            raise ArgModelMismatch(str(e))

        imgs: list[BuildImage] = []
        try:
            for image in images:
                if isinstance(image, bytes):
                    image = BytesIO(image)
                imgs.append(BuildImage.open(image))  # type: ignore
        except Exception as e:
            raise OpenImageFailed(str(e))

        values = {"images": imgs, "texts": texts, "args": model}
        return self.function(**values)

    def generate_preview(self, *, args: dict[str, Any] = {}) -> BytesIO:
        default_images = [random_image() for _ in range(self.params_type.min_images)]
        default_texts = (
            self.params_type.default_texts.copy()
            if (
                self.params_type.min_texts
                <= len(self.params_type.default_texts)
                <= self.params_type.max_texts
            )
            else [random_text() for _ in range(self.params_type.min_texts)]
        )

        def _generate_preview(images: list[bytes], texts: list[str]):
            try:
                return self.__call__(images=images, texts=texts, args=args)
            except TextOrNameNotEnough:
                texts.append(random_text())
                return _generate_preview(images, texts)

        return _generate_preview(default_images, default_texts)
