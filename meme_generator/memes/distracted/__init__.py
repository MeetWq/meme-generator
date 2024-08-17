from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def distracted(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "1.png")
    label = BuildImage.open(img_dir / "0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").square().resize((500, 500))
        return frame.copy().paste(img, below=True).paste(label, (140, 320), alpha=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "distracted",
    distracted,
    min_images=1,
    max_images=1,
    keywords=["注意力涣散"],
    tags=MemeTags.arknights,
    date_created=datetime(2022, 4, 20),
    date_modified=datetime(2023, 2, 14),
)
