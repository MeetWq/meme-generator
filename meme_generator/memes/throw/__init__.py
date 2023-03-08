import random
from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def throw(images: List[BuildImage], texts, args):
    img = (
        images[0]
        .convert("RGBA")
        .circle()
        .rotate(random.randint(1, 360))
        .resize((143, 143))
    )
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img, (15, 178), alpha=True)
    return frame.save_jpg()


add_meme("throw", throw, min_images=1, max_images=1, keywords=["丢", "扔"])
