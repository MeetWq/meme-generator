from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import make_png_or_gif

img_dir = Path(__file__).parent / "images"


def plana_eat(images: list[BuildImage], texts, args):
    jerry = BuildImage.open(img_dir / "0.png").convert("RGBA")

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").circle().resize((488, 488), keep_ratio=True)
        return jerry.copy().paste(img, (212, 535), below=True)

    return make_png_or_gif(images, make)


add_meme(
    "plana_eat",
    plana_eat,
    min_images=1,
    max_images=1,
    keywords=["普拉娜吃", "普拉娜舔"],
    tags=MemeTags.plana,
    date_created=datetime(2024, 11, 21),
    date_modified=datetime(2024, 11, 21),
)
