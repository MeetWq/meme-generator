from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import make_png_or_gif

img_dir = Path(__file__).parent / "images"


def haruhi_raise(images: list[BuildImage], texts: list[str], args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize((250, 180), keep_ratio=True)
        return frame.copy().paste(
            img.perspective(((0, 51), (204, 0), (211, 147), (17, 217))),
            (429, 79),
            below=True,
        )

    return make_png_or_gif(images, make)


add_meme(
    "haruhi_raise",
    haruhi_raise,
    min_images=1,
    max_images=1,
    keywords=["凉宫春日举"],
    tags=MemeTags.haruhi,
    date_created=datetime(2024, 11, 13),
    date_modified=datetime(2024, 11, 13),
)
