from typing import List
from pathlib import Path
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif


img_dir = Path(__file__).parent / "images"


def need(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").square().resize((115, 115))
    frame = BuildImage.open(img_dir / "0.png")

    def make(img: BuildImage) -> BuildImage:
        return frame.copy().paste(
            img.square().resize((115, 115)), (327, 232), below=True
        )

    return make_jpg_or_gif(images[0], make)


add_meme("need", need, min_images=1, max_images=1, keywords=["需要", "你可能需要"])
