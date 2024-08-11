from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def perfect(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")
    img = images[0].convert("RGBA").resize((310, 460), keep_ratio=True, inside=True)
    frame.paste(img, (313, 64), alpha=True)
    return frame.save_jpg()


add_meme(
    "perfect",
    perfect,
    min_images=1,
    max_images=1,
    keywords=["完美"],
    date_created=datetime(2022, 3, 10),
    date_modified=datetime(2023, 2, 14),
)
