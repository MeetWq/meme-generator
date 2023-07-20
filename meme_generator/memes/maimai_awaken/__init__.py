from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def maimai_awaken(images: List[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(img: BuildImage) -> BuildImage:
        img = img.convert("RGBA").square().resize((250, 250)).rotate(-25, expand=True)
        return frame.copy().paste(img, (134, 134), alpha=True, below=True)

    return make_jpg_or_gif(images[0], make)


add_meme(
    "maimai_awaken", maimai_awaken, min_images=1, max_images=1, keywords=["旅行伙伴觉醒"]
)
