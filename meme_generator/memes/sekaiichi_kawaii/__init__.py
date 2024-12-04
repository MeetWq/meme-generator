from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def sekaiichi_kawaii(images: list[BuildImage], texts: list[str], args):
    w, h = images[0].size
    if (w / h) > 1.155:
        fg = BuildImage.open(img_dir / "0.png")
        size = (810, 416)
    else:
        fg = BuildImage.open(img_dir / "1.png")
        size = (585, 810)
    white = BuildImage.new("RGBA", size, color=(255, 255, 255, 255))

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize(size, keep_ratio=True)
        frame = fg.copy().paste(
            white.copy().paste(img, (0, 0), alpha=True),
            (45, 45),
            alpha=True,
            below=True,
        )
        return frame

    return make_jpg_or_gif(images, make)


add_meme(
    "sekaiichi_kawaii",
    sekaiichi_kawaii,
    min_images=1,
    max_images=1,
    keywords=["世界第一可爱"],
    tags=MemeTags.kotone,
    date_created=datetime(2024, 12, 4),
    date_modified=datetime(2024, 12, 4),
)
