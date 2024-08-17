from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def add_chaos(images: list[BuildImage], texts, args):
    banner = BuildImage.open(img_dir / "0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        return imgs[0].convert("RGBA").resize_width(240).paste(banner)

    return make_jpg_or_gif(images, make)


add_meme(
    "add_chaos",
    add_chaos,
    min_images=1,
    max_images=1,
    keywords=["添乱", "给社会添乱"],
    date_created=datetime(2023, 6, 21),
    date_modified=datetime(2023, 6, 21),
)
