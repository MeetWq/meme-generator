from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def fight_with_sunuo(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("L").resize((565, 1630), keep_ratio=True)
        return frame.copy().paste(img, (0, 245), below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "fight_with_sunuo",
    fight_with_sunuo,
    min_images=1,
    max_images=1,
    keywords=["我打宿傩", "我打宿傩吗"],
    tags=MemeTags.sukuna,
    date_created=datetime(2024, 4, 3),
    date_modified=datetime(2024, 5, 25),
)
