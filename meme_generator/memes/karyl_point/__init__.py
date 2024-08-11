from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags

img_dir = Path(__file__).parent / "images"


def karyl_point(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").rotate(7.5, expand=True).resize((225, 225))
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img, (87, 790), alpha=True)
    return frame.save_png()


add_meme(
    "karyl_point",
    karyl_point,
    min_images=1,
    max_images=1,
    keywords=["凯露指"],
    tags=MemeTags.karyl,
    date_created=datetime(2022, 11, 16),
    date_modified=datetime(2023, 2, 14),
)
