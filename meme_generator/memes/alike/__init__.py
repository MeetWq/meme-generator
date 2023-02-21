from typing import List
from pathlib import Path
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif


img_dir = Path(__file__).parent / "images"


def alike(images: List[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(img: BuildImage) -> BuildImage:
        return frame.copy().paste(
            img.resize((90, 90), keep_ratio=True), (131, 14), alpha=True
        )

    return make_jpg_or_gif(images[0], make)


add_meme("alike", alike, min_images=1, max_images=1, keywords=["一样"])
