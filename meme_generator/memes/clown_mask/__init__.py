from datetime import datetime
from typing import Literal
from pathlib import Path

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
from meme_generator import add_meme
from meme_generator.utils import make_png_or_gif


help_text = "小丑在前/后，before/behind"

class Model(MemeArgsModel):
    mode: Literal["before", "behind"] = Field("before", description=help_text)

args_type = MemeArgsType(
    args_model=Model,
    args_examples=[Model(mode="before"), Model(mode="behind")],
    parser_options=[
        ParserOption(
            names=["--mode"],
            args=[ParserArg(name="mode", value="str")],
            help_text=help_text,
        ),
        ParserOption(
            names=["--before","前"],
            dest="mode",
            action=store_value("before"),
            help_text="小丑在前",
        ),
        ParserOption(
            names=["--behind","后"],
            dest="mode",
            action=store_value("behind"),
            help_text="小丑在后",
        ),
    ]
)


img_dir = Path(__file__).parent / "images"

def clown_mask(images: list[BuildImage], texts: list[str], args:Model):
    def make1(imgs: list[BuildImage]) -> BuildImage:
        frame = BuildImage.open(img_dir / "0.png")
        img = imgs[0].convert("RGBA").circle().resize((440, 440)).rotate(15)
        return frame.copy().paste(
            img,
            (16,104),
            alpha=True,
            below=True
        )
    
    def make2(imgs: list[BuildImage]) -> BuildImage:
        frame1 = BuildImage.open(img_dir / "1.png")
        frame2 = BuildImage.open(img_dir / "2.png")
        img = imgs[0].convert("RGBA").circle().perspective(((282, 0), (496, 154), (214, 546), (0, 392))).rotate(6)
        frame1.paste(
            img,
            (214, 100),
            alpha=True,
            below=False
        )
        return frame1.paste(
            frame2,
            (-85, 20),
            alpha=True,
            below=False
        )
    if args.mode == "before":
        return make_png_or_gif(images, make1)
    return make_png_or_gif(images, make2)


add_meme(
    "clown_mask",
    clown_mask,
    min_images=1,
    max_images=1,
    keywords=["小丑面具"],
    args_type=args_type,
    shortcuts=[
        CommandShortcut(key="小丑面具前",args=["--before"]),
        CommandShortcut(key="小丑面具后",args=["--behind"]),
    ],
    date_created=datetime(2024, 9, 20),
    date_modified=datetime(2024, 9, 20),
)