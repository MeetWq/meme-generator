from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage
from pydantic import Field

from meme_generator import MemeArgsModel, MemeArgsParser, MemeArgsType, add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"

help = "是否将图片变为圆形"

parser = MemeArgsParser(prefix_chars="-/")
parser.add_argument("--circle", "/圆", action="store_true", help=help)


class Model(MemeArgsModel):
    circle: bool = Field(False, description=help)


def dog_dislike(images: List[BuildImage], texts: List[str], args: Model):
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
    frames: List[IMG] = []
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
    args_type=MemeArgsType(parser, Model, [Model(circle=False), Model(circle=True)]),
    keywords=["狗都不玩"],
)
