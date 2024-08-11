from datetime import datetime
from typing import Literal, NamedTuple

from arclet.alconna import store_value
from PIL.Image import Image as IMG
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
from meme_generator.utils import save_gif

help_text = "鬼畜对称方向，包含 left、right、top、bottom"


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
            names=["--left", "左"], dest="direction", action=store_value("left")
        ),
        ParserOption(
            names=["--right", "右"], dest="direction", action=store_value("right")
        ),
        ParserOption(
            names=["--top", "上"], dest="direction", action=store_value("top")
        ),
        ParserOption(
            names=["--bottom", "下"], dest="direction", action=store_value("bottom")
        ),
    ],
)


def guichu(images: list[BuildImage], texts, args: Model):
    img = images[0].convert("RGBA")
    img_w, img_h = img.size

    class Mode(NamedTuple):
        method: Transpose
        size1: tuple[int, int, int, int]
        pos1: tuple[int, int]
        size2: tuple[int, int, int, int]
        pos2: tuple[int, int]

    modes: dict[str, Mode] = {
        "left": Mode(
            Transpose.FLIP_LEFT_RIGHT,
            (0, 0, img_w // 2, img_h),
            (0, 0),
            (img_w // 2, 0, img_w // 2 * 2, img_h),
            (img_w // 2, 0),
        ),
        "right": Mode(
            Transpose.FLIP_LEFT_RIGHT,
            (img_w // 2, 0, img_w // 2 * 2, img_h),
            (img_w // 2, 0),
            (0, 0, img_w // 2, img_h),
            (0, 0),
        ),
        "top": Mode(
            Transpose.FLIP_TOP_BOTTOM,
            (0, 0, img_w, img_h // 2),
            (0, 0),
            (0, img_h // 2, img_w, img_h // 2 * 2),
            (0, img_h // 2),
        ),
        "bottom": Mode(
            Transpose.FLIP_TOP_BOTTOM,
            (0, img_h // 2, img_w, img_h // 2 * 2),
            (0, img_h // 2),
            (0, 0, img_w, img_h // 2),
            (0, 0),
        ),
    }
    mode = modes[args.direction]

    img_flip = img.transpose(mode.method)
    img_symmetric = BuildImage.new("RGBA", img.size)
    img_symmetric.paste(img.crop(mode.size1), mode.pos1, alpha=True)
    img_symmetric.paste(img_flip.crop(mode.size2), mode.pos2, alpha=True)
    img_symmetric_big = BuildImage.new("RGBA", img.size)
    img_symmetric_big.paste(
        img_symmetric.copy().resize_width(img_w * 2), (-img_w // 2, -img_h // 2)
    )

    frames: list[IMG] = []
    frames += (
        ([img.image] * 3 + [img_flip.image] * 3) * 3
        + [img.image, img_flip.image] * 3
        + ([img_symmetric.image] * 2 + [img_symmetric_big.image] * 2) * 2
    )

    return save_gif(frames, 0.20)


add_meme(
    "guichu",
    guichu,
    min_images=1,
    max_images=1,
    args_type=args_type,
    keywords=["鬼畜"],
    date_created=datetime(2023, 7, 19),
    date_modified=datetime(2023, 7, 19),
)
