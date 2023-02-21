from typing import List
from pathlib import Path
from pil_utils import BuildImage

from meme_generator import add_meme


img_dir = Path(__file__).parent / "images"


def gun(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").resize((500, 500), keep_ratio=True)
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img, below=True)
    return frame.save_jpg()


add_meme("gun", gun, min_images=1, max_images=1, keywords=["手枪"])
