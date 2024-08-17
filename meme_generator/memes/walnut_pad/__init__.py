from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def walnut_pad(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize((540, 360), keep_ratio=True)
        return frame.copy().paste(img, (368, 65), below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "walnut_pad",
    walnut_pad,
    min_images=1,
    max_images=1,
    keywords=["胡桃平板"],
    tags=MemeTags.walnut,
    date_created=datetime(2022, 8, 7),
    date_modified=datetime(2023, 2, 14),
)
