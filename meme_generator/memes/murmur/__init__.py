from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def murmur(images, texts: list[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.jpg")
    try:
        frame.draw_text(
            (10, 255, 430, 300),
            text,
            max_fontsize=40,
            min_fontsize=15,
        )
    except ValueError:
        raise TextOverLength(text)
    return frame.save_jpg()


add_meme(
    "murmur",
    murmur,
    min_texts=1,
    max_texts=1,
    default_texts=["你的假期余额不足"],
    keywords=["低语"],
    date_created=datetime(2021, 12, 31),
    date_modified=datetime(2023, 2, 14),
)
