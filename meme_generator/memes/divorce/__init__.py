from typing import List
from pathlib import Path
from pil_utils import BuildImage

from meme_generator import add_meme


img_dir = Path(__file__).parent / "images"


def divorce(images: List[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")
    img = images[0].convert("RGBA").resize(frame.size, keep_ratio=True)
    frame.paste(img, below=True)
    return frame.save_jpg()


add_meme("divorce", ["离婚协议", "离婚申请"], divorce, min_images=1, max_images=1)
