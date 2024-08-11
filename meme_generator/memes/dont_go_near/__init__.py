from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def dont_go_near(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(img: BuildImage) -> BuildImage:
        img = img.convert("RGBA").resize((170, 170), keep_ratio=True)
        return frame.copy().paste(img, (23, 231), alpha=True)

    return make_jpg_or_gif(images[0], make)


add_meme(
    "dont_go_near",
    dont_go_near,
    min_images=1,
    max_images=1,
    keywords=["不要靠近"],
    date_created=datetime(2022, 1, 2),
    date_modified=datetime(2023, 4, 20),
)
