from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def need(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").square().resize((115, 115))
        return frame.copy().paste(img, (327, 232), below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "need",
    need,
    min_images=1,
    max_images=1,
    keywords=["需要", "你可能需要"],
    date_created=datetime(2022, 3, 30),
    date_modified=datetime(2023, 2, 14),
)
