from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def police(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").square().resize((245, 245))
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img, (224, 46), below=True)
    return frame.save_jpg()


def police1(images: list[BuildImage], texts, args):
    img = (
        images[0]
        .convert("RGBA")
        .resize((60, 75), keep_ratio=True)
        .rotate(16, expand=True)
    )
    frame = BuildImage.open(img_dir / "1.png")
    frame.paste(img, (37, 291), below=True)
    return frame.save_jpg()


add_meme(
    "police",
    police,
    min_images=1,
    max_images=1,
    keywords=["出警"],
    date_created=datetime(2022, 2, 23),
    date_modified=datetime(2023, 2, 14),
)

add_meme(
    "police1",
    police1,
    min_images=1,
    max_images=1,
    keywords=["警察"],
    date_created=datetime(2022, 3, 12),
    date_modified=datetime(2023, 2, 14),
)
