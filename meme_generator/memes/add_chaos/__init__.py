from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def add_chaos(images: List[BuildImage], texts, args):
    banner = BuildImage.open(img_dir / "0.png")

    def make(img: BuildImage) -> BuildImage:
        return img.convert("RGBA").resize_width(240).paste(banner)

    return make_jpg_or_gif(images[0], make)


add_meme(
    "add_chaos",
    add_chaos,
    min_images=1,
    max_images=1,
    keywords=["添乱", "给社会添乱"],
)
