from datetime import datetime
from typing import Literal

from arclet.alconna import store_value
from pil_utils import BuildImage
from pydantic import Field

from meme_generator import (
    CommandShortcut,
    MemeArgsModel,
    MemeArgsType,
    ParserArg,
    ParserOption,
    add_meme,
)
from meme_generator.utils import (
    FrameAlignPolicy,
    Maker,
    make_gif_or_combined_gif,
    make_jpg_or_gif,
)

help_text = "生成模式，包含 normal、loop、circle"


class Model(MemeArgsModel):
    mode: Literal["normal", "loop", "circle"] = Field("normal", description=help_text)


args_type = MemeArgsType(
    args_model=Model,
    args_examples=[Model(mode="normal"), Model(mode="circle"), Model(mode="loop")],
    parser_options=[
        ParserOption(
            names=["--mode"],
            args=[ParserArg(name="mode", value="str")],
            help_text=help_text,
        ),
        ParserOption(
            names=["--circle", "套娃"],
            dest="mode",
            action=store_value("circle"),
            help_text="套娃模式",
        ),
        ParserOption(
            names=["--loop", "循环"],
            dest="mode",
            action=store_value("loop"),
            help_text="循环模式",
        ),
    ],
)


def always_normal(img: BuildImage):
    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0]
        img_big = img.convert("RGBA").resize_width(500)
        img_small = img.convert("RGBA").resize_width(100)
        h1 = img_big.height
        h2 = max(img_small.height, 80)
        frame = BuildImage.new("RGBA", (500, h1 + h2 + 10), "white")
        frame.paste(img_big, alpha=True).paste(
            img_small, (290, h1 + 5 + (h2 - img_small.height) // 2), alpha=True
        )
        frame.draw_text(
            (20, h1 + 5, 280, h1 + h2 + 5), "要我一直", halign="right", max_fontsize=60
        )
        frame.draw_text(
            (400, h1 + 5, 480, h1 + h2 + 5), "吗", halign="left", max_fontsize=60
        )
        return frame

    return make_jpg_or_gif([img], make)


def always_always(img: BuildImage, loop: bool = False):
    tmp_img = img.convert("RGBA").resize_width(500)
    img_h = tmp_img.height
    text_h = tmp_img.resize_width(100).height + tmp_img.resize_width(20).height + 10
    text_h = max(text_h, 80)
    frame_h = img_h + text_h
    text_frame = BuildImage.new("RGBA", (500, frame_h), "white")
    text_frame.draw_text(
        (0, img_h, 280, frame_h), "要我一直", halign="right", max_fontsize=60
    ).draw_text((400, img_h, 500, frame_h), "吗", halign="left", max_fontsize=60)

    frame_num = 20
    coeff = 5 ** (1 / frame_num)

    def maker(i: int) -> Maker:
        def make(imgs: list[BuildImage]) -> BuildImage:
            img = imgs[0].convert("RGBA").resize_width(500)
            base_frame = text_frame.copy().paste(img, alpha=True)
            frame = BuildImage.new("RGBA", base_frame.size, "white")
            r = coeff**i
            for _ in range(4):
                x = round(358 * (1 - r))
                y = round(frame_h * (1 - r))
                w = round(500 * r)
                h = round(frame_h * r)
                frame.paste(base_frame.resize((w, h)), (x, y))
                r /= 5
            return frame

        return make

    if not loop:
        return make_jpg_or_gif([img], maker(0))

    return make_gif_or_combined_gif(
        [img], maker, frame_num, 0.1, FrameAlignPolicy.extend_loop
    )


def always(images: list[BuildImage], texts, args: Model):
    img = images[0]
    mode = args.mode

    if mode == "normal":
        return always_normal(img)
    elif mode == "circle":
        return always_always(img, loop=False)
    else:
        return always_always(img, loop=True)


add_meme(
    "always",
    always,
    min_images=1,
    max_images=1,
    args_type=args_type,
    keywords=["一直"],
    shortcuts=[CommandShortcut(key="一直一直", args=["--loop"])],
    date_created=datetime(2021, 12, 2),
    date_modified=datetime(2024, 8, 9),
)
