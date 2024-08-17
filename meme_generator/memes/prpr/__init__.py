from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def prpr(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        points = ((0, 19), (236, 0), (287, 264), (66, 351))
        screen = (
            imgs[0]
            .convert("RGBA")
            .resize((330, 330), keep_ratio=True)
            .perspective(points)
        )
        return frame.copy().paste(screen, (56, 284), below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "prpr",
    prpr,
    min_images=1,
    max_images=1,
    keywords=["舔", "舔屏", "prpr"],
    date_created=datetime(2022, 3, 5),
    date_modified=datetime(2023, 2, 14),
)
