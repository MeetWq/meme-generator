from datetime import datetime
from pathlib import Path

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif
from pil_utils import BuildImage

img_dir = Path(__file__).parent / "images"


def sold_out(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        return frame.copy().paste(
            imgs[0].convert("RGBA").resize((960, 960), keep_ratio=True),
            (0, 0),
            below=True,
        )

    return make_jpg_or_gif(images, make)


add_meme(
    "sold_out",
    sold_out,
    min_images=1,
    max_images=1,
    keywords=["卖掉了"],
    date_created=datetime(2023, 3, 12),
    date_modified=datetime(2023, 3, 12),
)
