from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def maimai_awaken(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = (
            imgs[0].convert("RGBA").square().resize((250, 250)).rotate(-25, expand=True)
        )
        return frame.copy().paste(img, (134, 134), alpha=True, below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "maimai_awaken",
    maimai_awaken,
    min_images=1,
    max_images=1,
    keywords=["旅行伙伴觉醒"],
    tags=MemeTags.maimai,
    date_created=datetime(2023, 7, 19),
    date_modified=datetime(2023, 7, 19),
)
