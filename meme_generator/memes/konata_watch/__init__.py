from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import make_png_or_gif

img_dir = Path(__file__).parent / "images"


def konata_watch(images: list[BuildImage], texts: list[str], args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0]
        img = img.convert("RGBA").resize((510, 360), keep_ratio=True)
        return frame.copy().paste(
            img.perspective(((0, 0), (465, 0), (465, 340), (0, 360))),
            (44, 20),
            below=True,
        )

    return make_png_or_gif(images, make)


add_meme(
    "konata_watch",
    konata_watch,
    min_images=1,
    max_images=1,
    keywords=["泉此方看"],
    tags=MemeTags.konata,
    date_created=datetime(2024, 8, 18),
    date_modified=datetime(2024, 8, 18),
)
