from datetime import datetime
from pathlib import Path

from arclet.alconna import store_true
from PIL.Image import Image as IMG
from pil_utils import BuildImage
from pydantic import Field

from meme_generator import MemeArgsModel, MemeArgsType, ParserOption, add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"

help_text = "是否将图片变为圆形"


class Model(MemeArgsModel):
    circle: bool = Field(False, description=help_text)


args_type = MemeArgsType(
    args_model=Model,
    args_examples=[Model(circle=False), Model(circle=True)],
    parser_options=[
        ParserOption(
            names=["--circle", "圆"],
            default=False,
            action=store_true,
            help_text=help_text,
        ),
    ],
)


def dog_dislike(images: list[BuildImage], texts: list[str], args: Model):
    location = [
        (36, 408),
        (36, 410),
        (40, 375),
        (40, 355),
        (36, 325),
        (28, 305),
        (28, 305),
        (28, 305),
        (28, 305),
        (28, 285),
        (28, 285),
        (28, 285),
        (28, 285),
        (28, 290),
        (30, 295),
        (30, 300),
        (30, 300),
        (30, 300),
        (30, 300),
        (30, 300),
        (30, 300),
        (28, 298),
        (26, 296),
        (24, 294),
        (28, 294),
        (26, 294),
        (24, 294),
        (35, 294),
        (115, 330),
        (150, 355),
        (180, 420),
        (180, 450),
        (150, 450),
        (150, 450),
    ]
    head = images[0].convert("RGBA").resize((122, 122), keep_ratio=True)
    if args.circle:
        head = head.circle()
    frames: list[IMG] = []
    for i in range(34):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(head, location[i], alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.08)


add_meme(
    "dog_dislike",
    dog_dislike,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=0,
    args_type=args_type,
    keywords=["狗都不玩"],
    date_created=datetime(2023, 11, 16),
    date_modified=datetime(2023, 11, 16),
)
