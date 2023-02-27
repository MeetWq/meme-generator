import asyncio
import filetype
from pathlib import Path
from typing import List, Dict, Any
from argparse import ArgumentParser

from meme_generator.app import run_server
from meme_generator.meme import MemeArgsModel
from meme_generator.download import check_resources
from meme_generator.manager import get_meme, get_memes
from meme_generator.exception import NoSuchMeme, MemeGeneratorException


parser = ArgumentParser("meme")
subparsers = parser.add_subparsers(dest="handle")

list_parser = subparsers.add_parser("list", aliases=["ls"], help="get meme list")

show_parser = subparsers.add_parser("info", aliases=["show"], help="get meme info")
show_parser.add_argument("key", type=str, help="the key of the meme")

preview_parser = subparsers.add_parser("preview", help="get preview result of the meme")
preview_parser.add_argument("key", type=str, help="the key of the meme")

generate_parser = subparsers.add_parser(
    "generate", aliases=["make"], help="generate meme"
)
memes_subparsers = generate_parser.add_subparsers(dest="key")

run_parser = subparsers.add_parser(
    "run", aliases=["start"], help="run meme_generator server"
)

download_parser = subparsers.add_parser(
    "download", help="download builtin memes images"
)


def add_parsers():
    for meme in get_memes():
        meme_parser = (
            meme.params_type.args_type.parser
            if meme.params_type.args_type
            else ArgumentParser()
        )
        meme_parser.add_argument("-i", "--images", nargs="+", default=[])
        meme_parser.add_argument("-t", "--texts", nargs="+", default=[])
        memes_subparsers.add_parser(
            meme.key,
            parents=[meme_parser],
            add_help=False,
            prefix_chars=meme_parser.prefix_chars,
        )


def list_memes() -> str:
    memes = sorted(get_memes(), key=lambda meme: meme.key)
    return "\n".join(
        f"{i}. {meme.key} ({'/'.join(meme.keywords)})" for i, meme in enumerate(memes)
    )


def meme_info(key: str) -> str:
    try:
        meme = get_meme(key)
    except NoSuchMeme as e:
        return str(e)
    args_model = (
        meme.params_type.args_type.model
        if meme.params_type.args_type
        else MemeArgsModel
    )
    return (
        f"key: {meme.key}\n"
        f"keywords: {meme.keywords}\n"
        f"patterns: {meme.patterns}\n"
        "params:\n"
        f"  min_images: {meme.params_type.min_images}\n"
        f"  max_images: {meme.params_type.max_images}\n"
        f"  min_texts: {meme.params_type.min_texts}\n"
        f"  max_texts: {meme.params_type.max_texts}\n"
        f"  default_texts: {meme.params_type.default_texts}\n"
        f"  args: {args_model().json()}"
    )


def generate_meme_preview(key: str) -> str:
    try:
        meme = get_meme(key)
    except NoSuchMeme as e:
        return str(e)

    try:
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(meme.generate_preview())
        content = result.getvalue()
        ext = filetype.guess_extension(content)
        filename = f"result.{ext}"
        with open(filename, "wb") as f:
            f.write(content)
        return f'Generate successfully! The generated file is "{filename}"'
    except MemeGeneratorException as e:
        return str(e)


def generate_meme(
    key: str, images: List[str], texts: List[str], args: Dict[str, Any]
) -> str:
    try:
        meme = get_meme(key)
    except NoSuchMeme as e:
        return str(e)
    for image in images:
        if not Path(image).exists():
            return f'Image "{image}" does not exist!'
    try:
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(meme(images=images, texts=texts, args=args))
        content = result.getvalue()
        ext = filetype.guess_extension(content)
        filename = f"result.{ext}"
        with open(filename, "wb") as f:
            f.write(content)
        return f'Generate successfully! The generated file is "{filename}"'
    except MemeGeneratorException as e:
        return str(e)


def main():
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
        key: str = kwargs.pop("key")
        images: List[str] = kwargs.pop("images")
        texts: List[str] = kwargs.pop("texts")
        print(generate_meme(key, images, texts, kwargs))

    elif handle in ["run", "start"]:
        run_server()

    elif handle in ["download"]:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(check_resources())

    else:
        print(parser.format_help())


if __name__ == "__main__":
    main()
