from datetime import datetime
from pathlib import Path

from meme_generator import add_meme
from pil_utils import BuildImage

img_dir = Path(__file__).parent / "images"


def empathy(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(
        images[0].convert("RGBA").circle().resize((90, 90)).rotate(100),
        (210, 425),
        below=True,
    )
    return frame.save_jpg()


add_meme(
    "empathy",
    empathy,
    min_images=1,
    max_images=1,
    keywords=["换位思考"],
    date_created=datetime(2023, 4, 27),
    date_modified=datetime(2023, 4, 27),
)
