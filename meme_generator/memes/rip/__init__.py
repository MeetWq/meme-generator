from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def rip(images: List[BuildImage], texts, args):
    if len(images) >= 2:
        frame = BuildImage.open(img_dir / "1.png")
        self_img = images[0]
        user_img = images[1]
    else:
        frame = BuildImage.open(img_dir / "0.png")
        self_img = None
        user_img = images[0]

    user_img = user_img.convert("RGBA").square().resize((385, 385))
    if self_img:
        self_img = self_img.convert("RGBA").square().resize((230, 230))
        frame.paste(self_img, (408, 418), below=True)
    frame.paste(user_img.rotate(24, expand=True), (-5, 355), below=True)
    frame.paste(user_img.rotate(-11, expand=True), (649, 310), below=True)
    return frame.save_jpg()


add_meme("rip", rip, min_images=1, max_images=2, keywords=["撕"])
