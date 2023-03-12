from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def forbid (images: List[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")
    frame.copy().paste(img.resize((304, 324), keep_ratio=True), (0, 0), below=True)
    return frame.save_jpg()


add_meme("forbid", forbid, min_images=1, max_images=1, keywords=["禁止", "禁"])
