from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def china_flag(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA")
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img.resize(frame.size, keep_ratio=True), below=True)
    return frame.save_jpg()


add_meme(
    "china_flag",
    china_flag,
    min_images=1,
    max_images=1,
    keywords=["国旗"],
    date_created=datetime(2022, 3, 9),
    date_modified=datetime(2023, 2, 14),
)
