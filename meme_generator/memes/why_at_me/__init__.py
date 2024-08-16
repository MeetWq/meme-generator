from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags

img_dir = Path(__file__).parent / "images"


def why_at_me(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").resize((265, 265), keep_ratio=True)
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img.rotate(19), (42, 13), below=True)
    return frame.save_jpg()


add_meme(
    "why_at_me",
    why_at_me,
    min_images=1,
    max_images=1,
    keywords=["为什么@我"],
    tags=MemeTags.touhou,
    date_created=datetime(2022, 4, 14),
    date_modified=datetime(2023, 5, 3),
)
