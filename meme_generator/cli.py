import asyncio
import copy
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List

import filetype

from meme_generator.app import run_server
from meme_generator.config import meme_config
from meme_generator.download import check_resources
from meme_generator.exception import MemeGeneratorException, NoSuchMeme
from meme_generator.log import setup_logger
from meme_generator.manager import get_meme, get_memes

parser = ArgumentParser("meme")
subparsers = parser.add_subparsers(dest="handle")

list_parser = subparsers.add_parser("list", aliases=["ls"], help="查看表情列表")

show_parser = subparsers.add_parser("info", aliases=["show"], help="查看表情详情")
show_parser.add_argument("key", type=str, help="表情名")

preview_parser = subparsers.add_parser("preview", help="生成表情预览")
preview_parser.add_argument("key", type=str, help="表情名")

generate_parser = subparsers.add_parser("generate", aliases=["make"], help="制作表情")
memes_subparsers = generate_parser.add_subparsers(dest="key", help="表情名")

run_parser = subparsers.add_parser("run", aliases=["start"], help="启动 web server")

download_parser = subparsers.add_parser("download", help="下载内置表情图片")
download_parser.add_argument(
    "--url", type=str, help="指定资源链接", default=meme_config.resource.resource_url
)


def add_parsers():
    for meme in get_memes():
        meme_parser = (
            copy.deepcopy(meme.params_type.args_type.parser)
            if meme.params_type.args_type
            else ArgumentParser()
        )
        meme_parser.add_argument("--images", nargs="+", default=[], help="输入图片路径")
        meme_parser.add_argument("--texts", nargs="+", default=[], help="输入文字")
        memes_subparsers.add_parser(
            meme.key,
            parents=[meme_parser],
            add_help=False,
            prefix_chars=meme_parser.prefix_chars,
        )


def list_memes() -> str:
    memes = sorted(get_memes(), key=lambda meme: meme.key)
    return "\n".join(
        f"{i}. {meme.key} ({'/'.join(meme.keywords)})"
        for i, meme in enumerate(memes, start=1)
    )


def meme_info(key: str) -> str:
    try:
        meme = get_meme(key)
    except NoSuchMeme:
        return f'表情 "{key}" 不存在！'

    keywords = "、".join([f'"{keyword}"' for keyword in meme.keywords])

    patterns = "、".join([f'"{pattern}"' for pattern in meme.patterns])

    image_num = f"{meme.params_type.min_images}"
    if meme.params_type.max_images > meme.params_type.min_images:
        image_num += f" ~ {meme.params_type.max_images}"

    text_num = f"{meme.params_type.min_texts}"
    if meme.params_type.max_texts > meme.params_type.min_texts:
        text_num += f" ~ {meme.params_type.max_texts}"

    default_texts = ", ".join([f'"{text}"' for text in meme.params_type.default_texts])

    def arg_info(name: str, info: Dict[str, Any]) -> str:
        text = (
            f'        "{name}"\n'
            f"            描述：{info.get('description', '')}\n"
            f"            类型：`{info.get('type', '')}`\n"
            f"            默认值：`{info.get('default', '')}`"
        )
        if enum := info.get("enum", []):
            assert isinstance(enum, list)
            text += "\n            可选值：" + "、".join([f'"{e}"' for e in enum])
        return text

    if args := meme.params_type.args_type:
        model = args.model
        properties: Dict[str, Dict[str, Any]] = model.schema().get("properties", {})
        properties.pop("user_infos")
        args_info = "\n" + "\n".join(
            [arg_info(name, info) for name, info in properties.items()]
        )
    else:
        args_info = ""

    return (
        f"表情名：{meme.key}\n"
        + f"关键词：{keywords}\n"
        + (f"正则表达式：{patterns}\n" if patterns else "")
        + "参数：\n"
        + f"    需要图片数目：{image_num}\n"
        + f"    需要文字数目：{text_num}\n"
        + (f"    默认文字：[{default_texts}]\n" if default_texts else "")
        + (f"    其他参数：{args_info}\n" if args_info else "")
    )


def generate_meme_preview(key: str) -> str:
    try:
        meme = get_meme(key)
    except NoSuchMeme:
        return f'表情 "{key}" 不存在！'

    try:
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(meme.generate_preview())
        content = result.getvalue()
        ext = filetype.guess_extension(content)
        filename = f"result.{ext}"
        with open(filename, "wb") as f:
            f.write(content)
        return f'表情制作成功！生成的表情文件为 "{filename}"'
    except MemeGeneratorException as e:
        return str(e)


def generate_meme(
    key: str, images: List[str], texts: List[str], args: Dict[str, Any]
) -> str:
    try:
        meme = get_meme(key)
    except NoSuchMeme:
        return f'表情 "{key}" 不存在！'

    for image in images:
        if not Path(image).exists():
            return f'图片路径 "{image}" 不存在！'

    try:
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(meme(images=images, texts=texts, args=args))
        content = result.getvalue()
        ext = filetype.guess_extension(content)
        filename = f"result.{ext}"
        with open(filename, "wb") as f:
            f.write(content)
        return f'表情制作成功！生成的表情文件为 "{filename}"'
    except MemeGeneratorException as e:
        return str(e)


def main():
    setup_logger()
    add_parsers()

    args = parser.parse_args()
    handle = str(args.handle)

    if handle in ["list", "ls"]:
        print(list_memes())

    elif handle in ["info", "show"]:
        key = str(args.key)
        print(meme_info(key))

    elif handle in ["preview"]:
        key = str(args.key)
        print(generate_meme_preview(key))

    elif handle in ["generate", "make"]:
        kwargs = vars(args)
        kwargs.pop("handle")
        key: str = kwargs.pop("key")
        images: List[str] = kwargs.pop("images")
        texts: List[str] = kwargs.pop("texts")
        print(generate_meme(key, images, texts, kwargs))

    elif handle in ["run", "start"]:
        run_server()

    elif handle in ["download"]:
        meme_config.resource.resource_url = args.url
        loop = asyncio.new_event_loop()
        loop.run_until_complete(check_resources())

    else:
        print(parser.format_help())


if __name__ == "__main__":
    main()
