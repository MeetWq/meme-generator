from datetime import datetime
from pathlib import Path

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif
from pil_utils import BuildImage

img_dir = Path(__file__).parent / "images"


def forbid(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        return frame.copy().paste(
            imgs[0].convert("RGBA").resize((304, 324), keep_ratio=True),
            (0, 0),
            below=True,
        )

    return make_jpg_or_gif(images, make)


add_meme(
    "forbid",
    forbid,
    min_images=1,
    max_images=1,
    keywords=["禁止", "禁"],
    date_created=datetime(2023, 3, 12),
    date_modified=datetime(2023, 3, 12),
)
