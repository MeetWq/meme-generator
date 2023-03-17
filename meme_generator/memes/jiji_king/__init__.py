import math
from pathlib import Path
from typing import List

from pil_utils import BuildImage
from pydantic import Field

from meme_generator import MemeArgsModel, MemeArgsParser, MemeArgsType, add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"

help = "是否将图片变为圆形"

parser = MemeArgsParser(prefix_chars="-/")
parser.add_argument("--circle", "/圆", action="store_true", help=help)


class Model(MemeArgsModel):
    circle: bool = Field(False, description=help)


def jiji_king(images: List[BuildImage], texts: List[str], args: Model):
    block_num = 5
    if len(images) >= 7 or len(texts) >= 7:
        block_num = max(len(images), len(texts)) - 1

    chars = ["急"]
    text = "我是急急国王"

    if len(texts) == 1:
        if len(images) == 1:
            chars = [texts[0]] * block_num
            text = f"我是{texts[0]*2}国王"
        else:
            text = texts[0]
    elif len(texts) == 2:
        chars = [texts[0]] * block_num
        text = texts[1]
    elif texts:
        chars = sum(
            [[arg] * math.ceil(block_num / len(texts[:-1])) for arg in texts[:-1]], []
        )
        text = texts[-1]

    frame = BuildImage.new("RGBA", (10 + 100 * block_num, 400), "white")
    king = BuildImage.open(img_dir / "0.png")
    head = images[0].convert("RGBA").square().resize((125, 125))
    if args.circle:
        head = head.circle()
    king.paste(head, (237, 5), alpha=True)
    frame.paste(king, ((frame.width - king.width) // 2, 0))

    if len(images) > 1:
        imgs = images[1:]
        imgs = [img.convert("RGBA").square().resize((90, 90)) for img in imgs]
    else:
        imgs = []
        for char in chars:
            block = BuildImage.new("RGBA", (90, 90), "black")
            try:
                block.draw_text(
                    (0, 0, 90, 90),
                    char,
                    lines_align="center",
                    weight="bold",
                    max_fontsize=60,
                    min_fontsize=30,
                    fill="white",
                )
            except ValueError:
                raise TextOverLength(char)
            imgs.append(block)

    imgs = sum([[img] * math.ceil(block_num / len(imgs)) for img in imgs], [])
    for i in range(block_num):
        frame.paste(imgs[i], (10 + 100 * i, 200))

    try:
        frame.draw_text(
            (10, 300, frame.width - 10, 390),
            text,
            lines_align="center",
            weight="bold",
            max_fontsize=100,
            min_fontsize=30,
        )
    except ValueError:
        raise TextOverLength(text)

    return frame.save_jpg()


add_meme(
    "jiji_king",
    jiji_king,
    min_images=1,
    max_images=11,
    min_texts=0,
    max_texts=11,
    args_type=MemeArgsType(parser, Model, [Model(circle=False), Model(circle=True)]),
    keywords=["急急国王"],
)
