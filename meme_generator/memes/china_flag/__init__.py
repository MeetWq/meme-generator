from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def china_flag(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA")
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img.resize(frame.size, keep_ratio=True), below=True)
    return frame.save_jpg()


add_meme("china_flag", china_flag, min_images=1, max_images=1, keywords=["国旗"])
