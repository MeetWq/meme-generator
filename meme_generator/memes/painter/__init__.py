from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def painter(images: List[BuildImage], texts, args):
    img = (
        images[0].convert("RGBA").resize((240, 345), keep_ratio=True, direction="north")
    )
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img, (125, 91), below=True)
    return frame.save_jpg()


add_meme("painter", painter, min_images=1, max_images=1, keywords=["小画家"])
