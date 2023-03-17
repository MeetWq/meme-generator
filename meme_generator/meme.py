import copy
from argparse import ArgumentError, ArgumentParser
from contextvars import ContextVar
from dataclasses import dataclass, field
from io import BytesIO
from pathlib import Path
from typing import (
    IO,
    Any,
    Awaitable,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Type,
    TypeVar,
    Union,
    cast,
)

from pil_utils import BuildImage
from pydantic import BaseModel, ValidationError

from .exception import (
    ArgModelMismatch,
    ArgParserExit,
    ImageNumberMismatch,
    OpenImageFailed,
    ParserExit,
    TextNumberMismatch,
    TextOrNameNotEnough,
)
from .utils import is_coroutine_callable, random_image, random_text, run_sync


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


parser_message: ContextVar[str] = ContextVar("parser_message")


class MemeArgsParser(ArgumentParser):
    """`shell_like` 命令参数解析器，解析出错时不会退出程序。

    用法:
        用法与 `argparse.ArgumentParser` 相同，
        参考文档: [argparse](https://docs.python.org/3/library/argparse.html)
    """

    def _print_message(self, message: str, file: Optional[IO[str]] = None):
        if (msg := parser_message.get(None)) is not None:
            parser_message.set(msg + message)
        else:
            super()._print_message(message, file)

    def exit(self, status: int = 0, message: Optional[str] = None):
        if message:
            self._print_message(message)
        raise ParserExit(status=status, error_message=parser_message.get(None))


@dataclass
class MemeArgsType:
    parser: MemeArgsParser
    model: Type[MemeArgsModel]
    instances: List[MemeArgsModel] = field(default_factory=list)


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
            raise OpenImageFailed(str(e))

        values = {"images": imgs, "texts": texts, "args": model}

        if is_coroutine_callable(self.function):
            return await cast(Callable[..., Awaitable[BytesIO]], self.function)(
                **values
            )
        else:
            return await run_sync(cast(Callable[..., BytesIO], self.function))(**values)

    def parse_args(self, args: List[str] = []) -> Dict[str, Any]:
        parser = (
            copy.deepcopy(self.params_type.args_type.parser)
            if self.params_type.args_type
            else MemeArgsParser()
        )
        parser.add_argument("texts", nargs="*", default=[])
        t = parser_message.set("")
        try:
            return vars(parser.parse_args(args))
        except ArgumentError as e:
            raise ArgParserExit(self.key, str(e))
        except ParserExit as e:
            raise ArgParserExit(self.key, e.error_message)
        finally:
            parser_message.reset(t)

    async def generate_preview(self, *, args: Dict[str, Any] = {}) -> BytesIO:
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

        async def _generate_preview(images: List[BytesIO], texts: List[str]):
            try:
                return await self.__call__(images=images, texts=texts, args=args)
            except TextOrNameNotEnough:
                texts.append(random_text())
                return await _generate_preview(images, texts)

        return await _generate_preview(default_images, default_texts)
