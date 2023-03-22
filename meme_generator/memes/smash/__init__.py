from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def smash(images: List[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(img: BuildImage) -> BuildImage:
        points = ((1, 237), (826, 1), (832, 508), (160, 732))
        screen = (
            img.convert("RGBA").resize((800, 500), keep_ratio=True).perspective(points)
        )
        return frame.copy().paste(screen, (-136, -81), below=True)

    return make_jpg_or_gif(images[0], make)


add_meme("smash", smash, min_images=1, max_images=1, keywords=["砸"])
