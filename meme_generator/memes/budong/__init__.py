from datetime import datetime

from pil_utils import BuildImage
from pathlib import Path

from meme_generator import MemeArgsModel, add_meme

img_dir = Path(__file__).parent / "images"

def budong(images: list[BuildImage], texts: list[str], args: MemeArgsModel):
    frame = BuildImage.open(img_dir / "0.png")
    img = images[0].convert("RGBA").resize((155, 155), keep_ratio=True)

    frame.paste(img, (221, 182), below=True)

    return frame.save_jpg()


add_meme(
    "budong",
    budong,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=0,
    keywords=["不懂"],
    date_created=datetime(2022, 1, 1),
    date_modified=datetime(2023, 2, 14),
)
