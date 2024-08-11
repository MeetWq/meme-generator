from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def decent_kiss(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").resize((589, 340), keep_ratio=True)
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img, (0, 91), below=True)
    return frame.save_jpg()


add_meme(
    "decent_kiss",
    decent_kiss,
    min_images=1,
    max_images=1,
    keywords=["像样的亲亲"],
    date_created=datetime(2022, 4, 14),
    date_modified=datetime(2023, 2, 14),
)
