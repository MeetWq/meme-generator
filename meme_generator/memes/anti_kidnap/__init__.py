from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def anti_kidnap(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").resize((450, 450), keep_ratio=True)
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img, (30, 78), below=True)
    return frame.save_jpg()


add_meme("anti_kidnap", anti_kidnap, min_images=1, max_images=1, keywords=["防诱拐"])
