from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def erised_mirror(images: list[BuildImage], texts: list[str], args):
    frame = BuildImage.open(img_dir / "0.jpg")

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize((360, 207), keep_ratio=True)
        return frame.paste(
            img.perspective(((0, 0), (360, 0), (367, 207), (7, 207))),
            (55, 578),
            alpha=True,
        )

    return make_jpg_or_gif(images, make)


add_meme(
    "erised_mirror",
    erised_mirror,
    min_images=1,
    max_images=1,
    keywords=["意若思镜"],
    date_created=datetime(2024, 8, 31),
    date_modified=datetime(2024, 8, 31),
)
