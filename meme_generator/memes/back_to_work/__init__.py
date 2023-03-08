from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def back_to_work(images: List[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")
    img = (
        images[0].convert("RGBA").resize((220, 310), keep_ratio=True, direction="north")
    )
    frame.paste(img.rotate(25, expand=True), (56, 32), below=True)
    return frame.save_jpg()


add_meme(
    "back_to_work", back_to_work, min_images=1, max_images=1, keywords=["继续干活", "打工人"]
)
