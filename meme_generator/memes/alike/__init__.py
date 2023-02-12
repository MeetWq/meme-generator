from typing import List
from pathlib import Path
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif


img_dir = Path(__file__).parent / "images"


def alike(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").square().resize((90, 90))
    frame = BuildImage.open(img_dir / "0.png")

    def make(img: BuildImage) -> BuildImage:
        return frame.copy().paste(img, (131, 14), alpha=True)

    return make_jpg_or_gif(img, make)


add_meme("alike", ["一样"], alike, min_images=1, max_images=1)
