from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def frieren_take(images: List[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(img: BuildImage) -> BuildImage:
        img = img.convert("RGBA").resize((102, 108), keep_ratio=True)
        return frame.copy().paste(img, (130, 197), below=True)

    return make_jpg_or_gif(images[0], make)


add_meme("frieren_take", frieren_take, min_images=1, max_images=1, keywords=["芙莉莲拿"])
