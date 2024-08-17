from datetime import datetime
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
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

help_text = "跑动方向，包含 left_right、right_left"


class Model(MemeArgsModel):
    direction: Literal["left_right", "right_left"] = Field(
        "left_right", description=help_text
    )


args_type = MemeArgsType(
    args_model=Model,
    args_examples=[Model(direction="left_right"), Model(direction="right_left")],
    parser_options=[
        ParserOption(
            names=["-d", "--direction"],
            args=[ParserArg(name="direction", value="str")],
            help_text=help_text,
        ),
        ParserOption(
            names=["--left_right", "左右"],
            dest="direction",
            action=store_value("left_right"),
        ),
        ParserOption(
            names=["--right_left", "右左"],
            dest="direction",
            action=store_value("right_left"),
        ),
    ],
)


def left_right_jump(images: list[BuildImage], texts, args: Model):
    img_w = 100
    img_h = images[0].resize_width(img_w).height
    frame_w = 300
    frame_h = img_h + 30
    frame = BuildImage.new("RGBA", (frame_w, frame_h))

    def traj(x: float) -> float:
        h = 15
        w = (frame_w - img_w) / 4
        k = h / w**2
        if x < img_w / 2 or x > frame_w - img_w / 2:
            return 0
        elif x < frame_w / 2:
            return h - k * (x - img_w / 2 - w) ** 2
        else:
            return h - k * (x - img_w / 2 - w * 3) ** 2

    frame_num = 30
    dx = (frame_w - img_w) / (frame_num / 2 - 1)

    def maker(i: int) -> Maker:
        def make(imgs: list[BuildImage]) -> BuildImage:
            img = imgs[0].convert("RGBA").resize_width(img_w)
            if args.direction == "left_right":
                if i >= round(frame_num / 2):
                    x = frame_w - img_w - dx * (frame_num - i - 1)
                    img = img.transpose(Transpose.FLIP_LEFT_RIGHT)
                else:
                    x = frame_w - img_w - dx * i
            else:
                if i >= round(frame_num / 2):
                    x = dx * (frame_num - i - 1)
                    img = img.transpose(Transpose.FLIP_LEFT_RIGHT)
                else:
                    x = dx * i
            y = frame_h - (traj(x + img_w / 2) + img_h)
            return frame.copy().paste(img, (round(x), round(y)), alpha=True)

        return make

    return make_gif_or_combined_gif(
        images, maker, frame_num, 0.04, FrameAlignPolicy.extend_loop
    )


add_meme(
    "left_right_jump",
    left_right_jump,
    min_images=1,
    max_images=1,
    args_type=args_type,
    keywords=["左右横跳"],
    date_created=datetime(2024, 7, 14),
    date_modified=datetime(2024, 7, 14),
)
