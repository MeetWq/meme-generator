from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def daynight(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").resize((333, 360), keep_ratio=True)
    img_ = images[1].convert("RGBA").resize((333, 360), keep_ratio=True)
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img, (349, 0))
    frame.paste(img_, (349, 361))
    return frame.save_jpg()


add_meme(
    "daynight",
    daynight,
    min_images=2,
    max_images=2,
    keywords=["白天黑夜", "白天晚上"],
    date_created=datetime(2023, 10, 3),
    date_modified=datetime(2023, 10, 3),
)
