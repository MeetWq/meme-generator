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


help_text = "枪的位置，包含 left、right、both"


class Model(MemeArgsModel):
    position: Literal["left", "right", "both"] = Field("left", description=help_text)


args_type = MemeArgsType(
    args_model=Model,
    args_examples=[
        Model(position="left"),
        Model(position="right"),
        Model(position="both"),
    ],
    parser_options=[
        ParserOption(
            names=["-p", "--position"],
            args=[ParserArg(name="position", value="str")],
            help_text=help_text,
        ),
        ParserOption(
            names=["--left", "左手"], dest="position", action=store_value("left")
        ),
        ParserOption(
            names=["--right", "右手"], dest="position", action=store_value("right")
        ),
        ParserOption(
            names=["--both", "双手"], dest="position", action=store_value("both")
        ),
    ],
)


def gun(images: list[BuildImage], texts, args: Model):
    frame = images[0].convert("RGBA").resize((500, 500), keep_ratio=True)
    gun = BuildImage.open(img_dir / "0.png")
    position = args.position
    left = position in ["left", "both"]
    right = position in ["right", "both"]
    if left:
        frame.paste(gun, alpha=True)
    if right:
        frame.paste(gun.transpose(Transpose.FLIP_LEFT_RIGHT), alpha=True)
    return frame.save_jpg()


add_meme(
    "gun",
    gun,
    min_images=1,
    max_images=1,
    args_type=args_type,
    keywords=["手枪"],
    date_created=datetime(2022, 8, 22),
    date_modified=datetime(2023, 2, 14),
)
