from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def dog_of_vtb(images: List[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(img: BuildImage) -> BuildImage:
        points = ((0, 0), (579, 0), (584, 430), (5, 440))
        img = img.convert("RGBA").resize((600, 450), keep_ratio=True)
        return frame.copy().paste(img.perspective(points), (97, 32), below=True)

    return make_jpg_or_gif(images[0], make)


add_meme(
    "dog_of_vtb",
    dog_of_vtb,
    min_images=1,
    max_images=1,
    keywords=["管人痴"],
)
