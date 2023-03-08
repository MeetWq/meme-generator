from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def hold_tight(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").resize((159, 171), keep_ratio=True)
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img, (113, 205), below=True)
    return frame.save_jpg()


add_meme("hold_tight", hold_tight, min_images=1, max_images=1, keywords=["抱紧"])
