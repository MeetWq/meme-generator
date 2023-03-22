from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def think_what(images: List[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(img: BuildImage) -> BuildImage:
        img = img.convert("RGBA").resize((534, 493), keep_ratio=True)
        return frame.copy().paste(img, (530, 0), below=True)

    return make_jpg_or_gif(images[0], make)


add_meme("think_what", think_what, min_images=1, max_images=1, keywords=["想什么"])
