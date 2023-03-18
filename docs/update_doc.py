import asyncio
from pathlib import Path
from typing import Any, Dict

import filetype

from meme_generator import get_memes
from meme_generator.meme import Meme

memes = sorted(get_memes(), key=lambda meme: meme.key)

image_path = Path("docs/images")


async def generate_preview_images():
    for meme in memes:

        async def generate_image(name: str, args: Dict[str, Any] = {}):
            for path in image_path.iterdir():
                if name == path.stem:
                    return

            result = await meme.generate_preview(args=args)
            content = result.getvalue()
            ext = filetype.guess_extension(content)
            filename = f"{name}.{ext}"
            with open(image_path / filename, "wb") as f:
                f.write(content)

        await generate_image(f"{meme.key}")
        if args := meme.params_type.args_type:
            if instances := args.instances:
                for i, instance in enumerate(instances):
                    await generate_image(f"{meme.key}_instance{i}", instance.dict())


def meme_doc(meme: Meme) -> str:
    keywords = "、".join([f"`{keyword}`" for keyword in meme.keywords])

    patterns = "、".join([f"`{pattern}`" for pattern in meme.patterns])

    image_num = f"`{meme.params_type.min_images}`"
    if meme.params_type.max_images > meme.params_type.min_images:
        image_num += f" ~ `{meme.params_type.max_images}`"

    text_num = f"`{meme.params_type.min_texts}`"
    if meme.params_type.max_texts > meme.params_type.min_texts:
        text_num += f" ~ `{meme.params_type.max_texts}`"

    default_texts = (
        f"{', '.join([f'`{text}`' for text in meme.params_type.default_texts])}"
    )

    def arg_info(name: str, info: Dict[str, Any]) -> str:
        text = (
            f"    - `{name}`\n"
            f"        - 描述：{info.get('description', '')}\n"
            f"        - 类型：`{info.get('type', '')}`\n"
            f"        - 默认值：`{info.get('default', '')}`"
        )
        if enum := info.get("enum", []):
            assert isinstance(enum, list)
            text += f"\n        - 可选值：{'、'.join([f'`{e}`' for e in enum])}"
        return text

    if args := meme.params_type.args_type:
        model = args.model
        properties: Dict[str, Dict[str, Any]] = (
            model.schema().get("properties", {}).copy()
        )
        properties.pop("user_infos")
        args_info = "\n" + "\n".join(
            [arg_info(name, info) for name, info in properties.items()]
        )
    else:
        args_info = ""

    if args := meme.params_type.args_type:
        parser = args.parser
        parser_info = parser.format_help()
        parser_info = parser_info.replace("update_doc.py", f"meme generate {meme.key}")
    else:
        parser_info = ""

    def image_doc(name: str) -> str:
        for path in image_path.iterdir():
            if name == path.stem:
                img_path = path.relative_to(Path("docs"))
                return (
                    '<div align="left">\n'
                    f'  <img src="{img_path}" width="200" />\n'
                    "</div>"
                )
        return ""

    preview_image = ""
    if args := meme.params_type.args_type:
        if instances := args.instances:
            preview_image = "\n\n".join(
                [
                    f"> 参数：{instance.json(exclude={'user_infos'})}\n"
                    + image_doc(meme.key + f"_instance{i}")
                    for i, instance in enumerate(instances)
                ]
            )
    if not preview_image:
        preview_image = image_doc(meme.key)

    return (
        f"## {meme.key}\n\n"
        + f"- 关键词：{keywords}\n"
        + (f"- 正则表达式：{patterns}\n" if patterns else "")
        + f"- 需要图片数目：{image_num}\n"
        + f"- 需要文字数目：{text_num}\n"
        + (f"- 默认文字：[{default_texts}]\n" if default_texts else "")
        + (f"- 其他参数：{args_info}\n" if args_info else "")
        + (f"- 其他参数（命令行选项）：\n```shell\n{parser_info}```\n\n" if parser_info else "")
        + "- 预览：\n"
        + f"{preview_image}"
    )


def generate_toc():
    return "\n".join(
        f"{i}. [{meme.key} ({'/'.join(meme.keywords)})](#{meme.key})"
        for i, meme in enumerate(memes, start=1)
    )


def generate_doc():
    doc = "# 表情列表\n\n以下为内置表情的关键词、所需参数等信息及表情预览\n\n按照表情的 `key` 排列\n\n\n"
    doc += generate_toc() + "\n\n\n"
    doc += "\n\n".join(meme_doc(meme) for meme in memes) + "\n"
    with open("docs/memes.md", "w") as f:
        f.write(doc)


async def main():
    await generate_preview_images()
    generate_doc()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
