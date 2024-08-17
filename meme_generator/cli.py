import asyncio
from pathlib import Path
from typing import Any

import filetype
from arclet.alconna import (
    Alconna,
    Args,
    CommandMeta,
    MultiVar,
    Option,
    Subcommand,
    TextFormatter,
)
from arclet.alconna.exceptions import SpecialOptionTriggered
from arclet.alconna.tools import RichConsoleFormatter

from meme_generator.app import run_server
from meme_generator.config import meme_config
from meme_generator.download import check_resources
from meme_generator.exception import MemeGeneratorException, NoSuchMeme
from meme_generator.log import setup_logger
from meme_generator.manager import get_meme, get_memes


def construct_parser() -> Alconna:
    sub_commands: list[Subcommand] = []
    for meme in get_memes():
        options: list[Option] = []
        if args_type := meme.params_type.args_type:
            for option in args_type.parser_options:
                options.append(option.option())
        sub_command = Subcommand(
            meme.key,
            *options,
            Option(
                "--images",
                Args["images", MultiVar(str, "+")],
                help_text="输入图片路径",
            ),
            Option("--texts", Args["texts", MultiVar(str, "+")], help_text="输入文字"),
            help_text="/".join(meme.keywords),
        )
        sub_commands.append(sub_command)

    parser = Alconna(
        "meme",
        Subcommand("list", alias=["ls"], help_text="查看表情列表"),
        Subcommand(
            "info", Args["key#表情名", str], alias=["show"], help_text="查看表情详情"
        ),
        Subcommand("preview", Args["key#表情名", str], help_text="生成表情预览"),
        Subcommand("generate", *sub_commands, alias=["make"], help_text="制作表情"),
        Subcommand("run", alias=["start"], help_text="启动 web server"),
        Subcommand(
            "download",
            Option("--url", Args["url", str], help_text="指定资源链接"),
            help_text="下载内置表情图片",
        ),
        meta=CommandMeta(
            description="表情包生成器",
            example="meme generate petpet --images /path/to/image/file",
        ),
        formatter_type=RichConsoleFormatter,
    )
    return parser


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
    shortcuts = "、".join(
        [f'"{shortcut.humanized or shortcut.key}"' for shortcut in meme.shortcuts]
    )
    tags = "、".join([f'"{tag}"' for tag in sorted(meme.tags)])

    image_num = f"{meme.params_type.min_images}"
    if meme.params_type.max_images > meme.params_type.min_images:
        image_num += f" ~ {meme.params_type.max_images}"

    text_num = f"{meme.params_type.min_texts}"
    if meme.params_type.max_texts > meme.params_type.min_texts:
        text_num += f" ~ {meme.params_type.max_texts}"

    default_texts = ", ".join([f'"{text}"' for text in meme.params_type.default_texts])

    args_info = ""
    if args_type := meme.params_type.args_type:
        formater = TextFormatter()
        for option in args_type.parser_options:
            opt = option.option()
            alias_text = (
                " ".join(opt.requires)
                + (" " if opt.requires else "")
                + "│".join(sorted(opt.aliases, key=len))
            )
            args_info += (
                f"\n  * {alias_text}{opt.separators[0]}"
                f"{formater.parameters(opt.args)} {opt.help_text}"
            )

    return (
        f"表情名：{meme.key}\n"
        + f"关键词：{keywords}\n"
        + (f"快捷指令：{shortcuts}\n" if shortcuts else "")
        + (f"标签：{tags}\n" if tags else "")
        + f"需要图片数目：{image_num}\n"
        + f"需要文字数目：{text_num}\n"
        + (f"默认文字：[{default_texts}]\n" if default_texts else "")
        + (f"其他参数：{args_info}" if args_info else "")
    )


def generate_meme_preview(key: str) -> str:
    try:
        meme = get_meme(key)
    except NoSuchMeme:
        return f'表情 "{key}" 不存在！'

    try:
        result = meme.generate_preview()
        content = result.getvalue()
        ext = filetype.guess_extension(content)
        filename = f"result.{ext}"
        with open(filename, "wb") as f:
            f.write(content)
        return f'表情制作成功！生成的表情文件为 "{filename}"'
    except MemeGeneratorException as e:
        return str(e)


def generate_meme(
    key: str, images: list[str], texts: list[str], args: dict[str, Any]
) -> str:
    try:
        meme = get_meme(key)
    except NoSuchMeme:
        return f'表情 "{key}" 不存在！'

    for image in images:
        if not Path(image).exists():
            return f'图片路径 "{image}" 不存在！'

    try:
        result = meme(images=images, texts=texts, args=args)
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
    parser = construct_parser()
    result = parser()

    if not result.matched:
        if not isinstance(result.error_info, SpecialOptionTriggered):
            print(result.error_info)  # noqa: T201
        return

    if not result.subcommands:
        print(parser.get_help())  # noqa: T201

    for subcommand, sub_result in result.subcommands.items():
        if subcommand == "list":
            print(list_memes())  # noqa: T201

        elif subcommand == "info":
            key = str(sub_result.args["key"])
            print(meme_info(key))  # noqa: T201

        elif subcommand == "preview":
            key = str(sub_result.args["key"])
            print(generate_meme_preview(key))  # noqa: T201

        elif subcommand == "generate":
            for key, subsub_result in sub_result.subcommands.items():
                images = (
                    list(subsub_result.options["images"].args["images"])
                    if "images" in subsub_result.options
                    else []
                )
                texts = (
                    list(subsub_result.options["texts"].args["texts"])
                    if "texts" in subsub_result.options
                    else []
                )
                options = subsub_result.options
                options.pop("images", None)
                options.pop("texts", None)
                args = {}
                for option, option_result in options.items():
                    if option_result.value is None:
                        args.update(option_result.args)
                    else:
                        args[option] = option_result.value
                print(generate_meme(key, images, texts, args))  # noqa: T201

        elif subcommand == "run":
            run_server()

        elif subcommand == "download":
            if "url" in sub_result.options:
                url = sub_result.options["url"].args["url"]
                meme_config.resource.resource_url = url
            loop = asyncio.new_event_loop()
            loop.run_until_complete(check_resources())


if __name__ == "__main__":
    main()
