from datetime import datetime
from pathlib import Path
from typing import Literal

from arclet.alconna import store_value
from PIL.Image import Transpose
from pil_utils import BuildImage
from pydantic import Field

from meme_generator import (
    MemeArgsModel,
    MemeArgsType,
    ParserArg,
    ParserOption,
    add_meme,
)

img_dir = Path(__file__).parent / "images"


help_text = "奶茶的位置，包含 right、left、both"


class Model(MemeArgsModel):
    position: Literal["right", "left", "both"] = Field("right", description=help_text)


args_type = MemeArgsType(
    args_model=Model,
    args_examples=[
        Model(position="right"),
        Model(position="left"),
        Model(position="both"),
    ],
    parser_options=[
        ParserOption(
            names=["-p", "--position"],
            args=[ParserArg(name="position", value="str")],
            help_text=help_text,
        ),
        ParserOption(
            names=["--right", "右手"], dest="position", action=store_value("right")
        ),
        ParserOption(
            names=["--left", "左手"], dest="position", action=store_value("left")
        ),
        ParserOption(
            names=["--both", "双手"], dest="position", action=store_value("both")
        ),
    ],
)


def bubble_tea(images: list[BuildImage], texts, args: Model):
    frame = images[0].convert("RGBA").resize((500, 500), keep_ratio=True)
    bubble_tea = BuildImage.open(img_dir / "0.png")
    position = args.position
    left = position in ["left", "both"]
    right = position in ["right", "both"]
    if right:
        frame.paste(bubble_tea, alpha=True)
    if left:
        frame.paste(bubble_tea.transpose(Transpose.FLIP_LEFT_RIGHT), alpha=True)
    return frame.save_jpg()


add_meme(
    "bubble_tea",
    bubble_tea,
    min_images=1,
    max_images=1,
    args_type=args_type,
    keywords=["奶茶"],
    date_created=datetime(2022, 8, 22),
    date_modified=datetime(2023, 3, 10),
)
