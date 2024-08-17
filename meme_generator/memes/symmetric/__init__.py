from datetime import datetime
from typing import Literal, NamedTuple

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
from meme_generator.utils import make_jpg_or_gif

help_text = "对称方向，包含 left、right、top、bottom"


class Model(MemeArgsModel):
    direction: Literal["left", "right", "top", "bottom"] = Field(
        "left", description=help_text
    )


args_type = MemeArgsType(
    args_model=Model,
    args_examples=[
        Model(direction="left"),
        Model(direction="right"),
        Model(direction="top"),
        Model(direction="bottom"),
    ],
    parser_options=[
        ParserOption(
            names=["-d", "--direction"],
            args=[ParserArg(name="direction", value="str")],
            help_text=help_text,
        ),
        ParserOption(
            names=["--left", "左"],
            dest="direction",
            action=store_value("left"),
        ),
        ParserOption(
            names=["--right", "右"],
            dest="direction",
            action=store_value("right"),
        ),
        ParserOption(
            names=["--top", "上"],
            dest="direction",
            action=store_value("top"),
        ),
        ParserOption(
            names=["--bottom", "下"],
            dest="direction",
            action=store_value("bottom"),
        ),
    ],
)


def symmetric(images: list[BuildImage], texts, args: Model):
    img_w, img_h = images[0].size

    class Mode(NamedTuple):
        method: Transpose
        frame_size: tuple[int, int]
        size1: tuple[int, int, int, int]
        pos1: tuple[int, int]
        size2: tuple[int, int, int, int]
        pos2: tuple[int, int]

    modes: dict[str, Mode] = {
        "left": Mode(
            Transpose.FLIP_LEFT_RIGHT,
            (img_w // 2 * 2, img_h),
            (0, 0, img_w // 2, img_h),
            (0, 0),
            (img_w // 2, 0, img_w // 2 * 2, img_h),
            (img_w // 2, 0),
        ),
        "right": Mode(
            Transpose.FLIP_LEFT_RIGHT,
            (img_w // 2 * 2, img_h),
            (img_w // 2, 0, img_w // 2 * 2, img_h),
            (img_w // 2, 0),
            (0, 0, img_w // 2, img_h),
            (0, 0),
        ),
        "top": Mode(
            Transpose.FLIP_TOP_BOTTOM,
            (img_w, img_h // 2 * 2),
            (0, 0, img_w, img_h // 2),
            (0, 0),
            (0, img_h // 2, img_w, img_h // 2 * 2),
            (0, img_h // 2),
        ),
        "bottom": Mode(
            Transpose.FLIP_TOP_BOTTOM,
            (img_w, img_h // 2 * 2),
            (0, img_h // 2, img_w, img_h // 2 * 2),
            (0, img_h // 2),
            (0, 0, img_w, img_h // 2),
            (0, 0),
        ),
    }

    mode = modes[args.direction]

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0]
        first = img.convert("RGBA")
        second = img.convert("RGBA").transpose(mode.method)
        frame = BuildImage.new("RGBA", mode.frame_size)
        frame.paste(first.crop(mode.size1), mode.pos1, alpha=True)
        frame.paste(second.crop(mode.size2), mode.pos2, alpha=True)
        return frame

    return make_jpg_or_gif(images, make)


add_meme(
    "symmetric",
    symmetric,
    min_images=1,
    max_images=1,
    args_type=args_type,
    keywords=["对称"],
    date_created=datetime(2022, 3, 14),
    date_modified=datetime(2023, 2, 14),
)
