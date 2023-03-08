from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def marriage(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").resize_height(1080)
    img_w, img_h = img.size
    if img_w > 1500:
        img_w = 1500
    elif img_w < 800:
        img_h = int(img_h * img_w / 800)
    frame = img.resize_canvas((img_w, img_h)).resize_height(1080)
    left = BuildImage.open(img_dir / "0.png")
    right = BuildImage.open(img_dir / "1.png")
    frame.paste(left, alpha=True).paste(
        right, (frame.width - right.width, 0), alpha=True
    )
    return frame.save_jpg()


add_meme("marriage", marriage, min_images=1, max_images=1, keywords=["结婚申请", "结婚登记"])
