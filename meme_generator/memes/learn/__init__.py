from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"

default_text = "偷学群友数理基础"


def learn(images: list[BuildImage], texts: list[str], args):
    text = texts[0] if texts else default_text
    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (100, 1360, frame.width - 100, 1730),
            text,
            max_fontsize=350,
            min_fontsize=200,
            weight="bold",
        )
    except ValueError:
        raise TextOverLength(text)

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize((1751, 1347), keep_ratio=True)
        return frame.copy().paste(img, (1440, 0), alpha=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "learn",
    learn,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=[default_text],
    keywords=["偷学"],
    date_created=datetime(2022, 12, 4),
    date_modified=datetime(2023, 2, 14),
)
