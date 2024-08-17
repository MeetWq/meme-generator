from datetime import datetime
from typing import Literal

from arclet.alconna import store_value
from pil_utils import BuildImage
from pydantic import Field

from meme_generator import (
    MemeArgsModel,
    MemeArgsType,
    ParserArg,
    ParserOption,
    add_meme,
)
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

help_text = "循环方向，包含 left、right、top、bottom"


class Model(MemeArgsModel):
    direction: Literal["left", "right", "top", "bottom"] = Field(
        "top", description=help_text
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


def loop(images: list[BuildImage], texts, args: Model):
    def maker(i: int) -> Maker:
        def make(imgs: list[BuildImage]) -> BuildImage:
            img = imgs[0].convert("RGBA")
            width, height = img.size

            if args.direction in ["top", "bottom"]:
                extend_img = BuildImage.new("RGBA", (width, height * 2), "white")
                extend_img.paste(img, (0, 0))
                extend_img.paste(img, (0, height))

                dh = round(height / 30 * i)
                if args.direction == "top":
                    return extend_img.crop((0, dh, width, dh + height))
                else:
                    return extend_img.crop((0, height - dh, width, height * 2 - dh))

            else:
                extend_img = BuildImage.new("RGBA", (width * 2, height), "white")
                extend_img.paste(img, (0, 0))
                extend_img.paste(img, (width, 0))

                dw = round(width / 30 * i)
                if args.direction == "left":
                    return extend_img.crop((dw, 0, dw + width, height))
                else:
                    return extend_img.crop((width - dw, 0, width * 2 - dw, height))

        return make

    return make_gif_or_combined_gif(
        images, maker, 30, 0.05, FrameAlignPolicy.extend_loop
    )


add_meme(
    "loop",
    loop,
    min_images=1,
    max_images=1,
    args_type=args_type,
    keywords=["循环"],
    date_created=datetime(2024, 7, 14),
    date_modified=datetime(2024, 8, 15),
)
