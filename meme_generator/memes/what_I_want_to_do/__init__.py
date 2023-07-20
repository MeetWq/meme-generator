from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def what_I_want_to_do(images: List[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(img: BuildImage) -> BuildImage:
        img = img.convert("RGBA").circle().resize((270, 270))
        return frame.copy().paste(img, (350, 590), alpha=True)

    return make_jpg_or_gif(images[0], make)


add_meme(
    "what_I_want_to_do",
    what_I_want_to_do,
    min_images=1,
    max_images=1,
    keywords=["我想上的"],
)
