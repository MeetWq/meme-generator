from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def paint(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").resize((117, 135), keep_ratio=True)
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img.rotate(4, expand=True), (95, 107), below=True)
    return frame.save_jpg()


add_meme(
    "paint",
    paint,
    min_images=1,
    max_images=1,
    keywords=["这像画吗"],
    date_created=datetime(2022, 3, 11),
    date_modified=datetime(2023, 2, 14),
)
