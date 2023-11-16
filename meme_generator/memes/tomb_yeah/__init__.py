from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def tomb_yeah(images: List[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.jpg").convert("RGBA")
    frame.paste(
        images[0].convert("RGBA").circle().resize((145, 145)), (138, 265), alpha=True
    )
    if len(images) > 1:
        frame.paste(
            images[1].convert("RGBA").circle().rotate(30).resize((145, 145)),
            (371, 312),
            alpha=True,
        )
    return frame.save_jpg()


add_meme("tomb_yeah", tomb_yeah, min_images=1, max_images=2, keywords=["上坟", "坟前比耶"])
