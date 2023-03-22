from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def prpr(images: List[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(img: BuildImage) -> BuildImage:
        points = ((0, 19), (236, 0), (287, 264), (66, 351))
        screen = (
            img.convert("RGBA").resize((330, 330), keep_ratio=True).perspective(points)
        )
        return frame.copy().paste(screen, (56, 284), below=True)

    return make_jpg_or_gif(images[0], make)


add_meme("prpr", prpr, min_images=1, max_images=1, keywords=["舔", "舔屏", "prpr"])
