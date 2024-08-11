from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def pinch(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(img: BuildImage) -> BuildImage:
        return frame.paste(
            img.convert("RGBA").resize((1800, 1440), keep_ratio=True),
            (1080, 0),
            below=True,
        )

    return make_jpg_or_gif(images[0], make)


add_meme(
    "pinch",
    pinch,
    min_images=1,
    max_images=1,
    keywords=["捏", "捏脸"],
    date_created=datetime(2023, 11, 18),
    date_modified=datetime(2023, 11, 18),
)
