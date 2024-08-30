from datetime import datetime
from pathlib import Path

from meme_generator import add_meme
from pil_utils import BuildImage

img_dir = Path(__file__).parent / "images"


def grab(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(
        images[0].convert("RGBA").resize((500, 500), keep_ratio=True), below=True
    )
    return frame.save_jpg()


add_meme(
    "grab",
    grab,
    min_images=1,
    max_images=1,
    keywords=["抓"],
    date_created=datetime(2023, 3, 28),
    date_modified=datetime(2023, 3, 28),
)
