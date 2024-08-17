from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def blood_pressure(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize((414, 450), keep_ratio=True)
        return frame.copy().paste(img, (16, 17), below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "blood_pressure",
    blood_pressure,
    min_images=1,
    max_images=1,
    keywords=["高血压"],
    date_created=datetime(2022, 8, 22),
    date_modified=datetime(2023, 2, 14),
)
