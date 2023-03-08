from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def perfect(images: List[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")
    img = images[0].convert("RGBA").resize((310, 460), keep_ratio=True, inside=True)
    frame.paste(img, (313, 64), alpha=True)
    return frame.save_jpg()


add_meme("perfect", perfect, min_images=1, max_images=1, keywords=["完美"])
