from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags

img_dir = Path(__file__).parent / "images"


def painter(images: list[BuildImage], texts, args):
    img = (
        images[0].convert("RGBA").resize((240, 345), keep_ratio=True, direction="north")
    )
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img, (125, 91), below=True)
    return frame.save_jpg()


add_meme(
    "painter",
    painter,
    min_images=1,
    max_images=1,
    keywords=["小画家"],
    tags=MemeTags.griseo,
    date_created=datetime(2022, 6, 4),
    date_modified=datetime(2023, 2, 14),
)
