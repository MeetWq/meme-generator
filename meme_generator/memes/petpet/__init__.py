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


def petpet(images: List[BuildImage], texts, args: Model):
    img = images[0].convert("RGBA").square()
    if args.circle:
        img = img.circle()

    frames: List[IMG] = []
    locs = [
        (14, 20, 98, 98),
        (12, 33, 101, 85),
        (8, 40, 110, 76),
        (10, 33, 102, 84),
        (12, 20, 98, 98),
    ]
    for i in range(5):
        hand = BuildImage.open(img_dir / f"{i}.png")
        frame = BuildImage.new("RGBA", hand.size, (255, 255, 255, 0))
        x, y, w, h = locs[i]
        frame.paste(img.resize((w, h)), (x, y), alpha=True)
        frame.paste(hand, alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.06)


add_meme(
    "petpet",
    petpet,
    min_images=1,
    max_images=1,
    args_type=MemeArgsType(parser, Model, [Model(circle=False), Model(circle=True)]),
    keywords=["摸", "摸摸", "摸头", "rua"],
)
