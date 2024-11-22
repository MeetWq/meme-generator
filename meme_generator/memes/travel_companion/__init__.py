from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def travel_companion(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").resize((370, 370), keep_ratio=True)
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img, (45, 45), below=True)
    return frame.save_jpg()


add_meme(
    "travel_companion",
    travel_companion,
    min_images=1,
    max_images=1,
    keywords=["新旅行伙伴", "旅行伙伴", "伙伴"],
    date_created=datetime(2024, 11, 6),
    date_modified=datetime(2024, 11, 22),
)
