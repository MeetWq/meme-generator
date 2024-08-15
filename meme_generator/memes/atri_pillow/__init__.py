import random
from datetime import datetime
from pathlib import Path
from typing import Literal

from arclet.alconna import store_value
from pil_utils import BuildImage
from pydantic import Field

from meme_generator import MemeArgsModel, MemeArgsType, ParserOption, add_meme
from meme_generator.exception import TextOverLength
from meme_generator.tags import MemeTags

img_dir = Path(__file__).parent / "images"


help_text = "yes or no"


class Model(MemeArgsModel):
    mode: Literal["yes", "no", "random"] = Field("random", description=help_text)


args_type = MemeArgsType(
    args_model=Model,
    args_examples=[Model(mode="yes"), Model(mode="no")],
    parser_options=[
        ParserOption(names=["-y", "--yes"], dest="mode", action=store_value("yes")),
        ParserOption(names=["-n", "--no"], dest="mode", action=store_value("no")),
    ],
)


def atri_pillow(images, texts: list[str], args: Model):
    text = texts[0]
    mode = args.mode
    if mode == "random":
        mode = random.choice(["yes", "no"])
    if mode == "yes":
        text_color = (255, 0, 0, 80)
    else:
        text_color = (0, 80, 255, 80)
    frame = BuildImage.open(img_dir / f"{mode}.png")
    text_img = BuildImage.new("RGBA", (300, 150))
    try:
        text_img.draw_text(
            (20, 20, 280, 130),
            text,
            max_fontsize=120,
            min_fontsize=30,
            allow_wrap=True,
            lines_align="center",
            fontname="FZShaoEr-M11S",
            fill=text_color,
        )
    except ValueError:
        raise TextOverLength(text)
    frame.alpha_composite(text_img.rotate(-4, expand=True), (302, 288))
    border = BuildImage.open(img_dir / "border.png")
    frame.paste(border, (0, 416))
    return frame.save_png()


add_meme(
    "atri_pillow",
    atri_pillow,
    min_texts=1,
    max_texts=1,
    default_texts=["ATRI"],
    args_type=args_type,
    keywords=["亚托莉枕头"],
    tags=MemeTags.atri,
    date_created=datetime(2024, 8, 12),
    date_modified=datetime(2024, 8, 15),
)
