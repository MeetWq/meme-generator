from pathlib import Path
from typing import List

from pil_utils import BuildImage
from pydantic import Field

from meme_generator import MemeArgsModel, MemeArgsParser, MemeArgsType, add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

help = "是否将图片变为圆形"

img_dir = Path(__file__).parent / "images"

parser = MemeArgsParser(prefix_chars="-/")
parser.add_argument("--circle", "/圆", action="store_true", help=help)


class Model(MemeArgsModel):
    circle: bool = Field(False, description=help)


def kirby_hammer(images: List[BuildImage], texts, args: Model):
    # fmt: off
    positions = [
        (318, 163), (319, 173), (320, 183), (317, 193), (312, 199), 
        (297, 212), (289, 218), (280, 224), (278, 223), (278, 220), 
        (280, 215), (280, 213), (280, 210), (280, 206), (280, 201), 
        (280, 192), (280, 188), (280, 184), (280, 179)
    ]
    # fmt: on
    def maker(i: int) -> Maker:
        def make(img: BuildImage) -> BuildImage:
            img = img.convert("RGBA")
            if args.circle:
                img = img.circle()
            img = img.resize_height(80)
            if img.width < 80:
                img = img.resize((80, 80), keep_ratio=True)
            frame = BuildImage.open(img_dir / f"{i}.png")
            if i <= 18:
                x, y = positions[i]
                x = x + 40 - img.width // 2
                frame.paste(img, (x, y), alpha=True)
            elif i <= 39:
                x, y = positions[18]
                x = x + 40 - img.width // 2
                frame.paste(img, (x, y), alpha=True)
            return frame

        return make

    return make_gif_or_combined_gif(
        images[0], maker, 62, 0.05, FrameAlignPolicy.extend_loop
    )


add_meme(
    "kirby_hammer",
    kirby_hammer,
    min_images=1,
    max_images=1,
    args_type=MemeArgsType(parser, Model, [Model(circle=False), Model(circle=True)]),
    keywords=["卡比锤", "卡比重锤"],
)
