from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def overtime(images: List[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")
    img = images[0].convert("RGBA").resize((250, 250), keep_ratio=True)
    frame.paste(img.rotate(-25, expand=True), (165, 220), below=True)
    return frame.save_jpg()


add_meme("overtime", overtime, min_images=1, max_images=1, keywords=["加班"])
