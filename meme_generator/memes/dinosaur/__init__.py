from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def dinosaur(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize((680, 578), keep_ratio=True)
        return frame.copy().paste(img, (294, 369), below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "dinosaur",
    dinosaur,
    min_images=1,
    max_images=1,
    keywords=["恐龙", "小恐龙"],
    date_created=datetime(2023, 1, 6),
    date_modified=datetime(2023, 2, 14),
)
