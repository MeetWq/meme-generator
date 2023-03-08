from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def karyl_point(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").rotate(7.5, expand=True).resize((225, 225))
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img, (87, 790), alpha=True)
    return frame.save_png()


add_meme("karyl_point", karyl_point, min_images=1, max_images=1, keywords=["凯露指"])
