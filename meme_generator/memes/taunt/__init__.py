from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def taunt(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").square().resize((230, 230))
        return frame.copy().paste(img, (245, 245))

    return make_jpg_or_gif(images, make)


add_meme(
    "taunt",
    taunt,
    min_images=1,
    max_images=1,
    keywords=["嘲讽"],
    date_created=datetime(2023, 7, 19),
    date_modified=datetime(2023, 7, 19),
)
