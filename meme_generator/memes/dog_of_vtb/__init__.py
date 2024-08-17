from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def dog_of_vtb(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        points = ((0, 0), (579, 0), (584, 430), (5, 440))
        img = imgs[0].convert("RGBA").resize((600, 450), keep_ratio=True)
        return frame.copy().paste(img.perspective(points), (97, 32), below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "dog_of_vtb",
    dog_of_vtb,
    min_images=1,
    max_images=1,
    keywords=["管人痴"],
    date_created=datetime(2023, 4, 18),
    date_modified=datetime(2023, 4, 18),
)
