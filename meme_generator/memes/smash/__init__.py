from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def smash(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        points = ((1, 237), (826, 1), (832, 508), (160, 732))
        screen = (
            imgs[0]
            .convert("RGBA")
            .resize((800, 500), keep_ratio=True)
            .perspective(points)
        )
        return frame.copy().paste(screen, (-136, -81), below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "smash",
    smash,
    min_images=1,
    max_images=1,
    keywords=["砸"],
    date_created=datetime(2022, 11, 29),
    date_modified=datetime(2023, 2, 14),
)
