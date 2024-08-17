from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def maimai_join(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").square().resize((400, 400))
        return frame.copy().paste(img, (50, 50), alpha=True, below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "maimai_join",
    maimai_join,
    min_images=1,
    max_images=1,
    keywords=["旅行伙伴加入"],
    tags=MemeTags.maimai,
    date_created=datetime(2023, 7, 19),
    date_modified=datetime(2023, 7, 19),
)
