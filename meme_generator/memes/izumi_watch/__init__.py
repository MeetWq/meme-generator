from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import make_png_or_gif

img_dir = Path(__file__).parent / "images"


def izumi_watch(images: list[BuildImage], texts: list[str], args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(img: BuildImage) -> BuildImage:
        img = img.convert("RGBA").resize((510, 360), keep_ratio=True)
        return frame.copy().paste(
            img.perspective(((0, 0), (465, 0), (465, 340), (0, 360))),
            (44, 20),
            below=True,
        )

    return make_png_or_gif(images[0], make)


add_meme(
    "izumi_watch",
    izumi_watch,
    min_images=1,
    max_images=1,
    keywords=["泉此方看"],
    tags=MemeTags.izumi,
    date_created=datetime(2024, 8, 18),
    date_modified=datetime(2024, 8, 18),
)
