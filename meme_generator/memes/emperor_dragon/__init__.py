from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def emperor_dragon(images, texts: list[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")

    try:
        frame.draw_text(
            (30, 440, 485, 512),
            text,
            allow_wrap=True,
            lines_align="center",
            min_fontsize=10,
            max_fontsize=100,
            fill=(0, 0, 0),
        )
    except ValueError:
        raise TextOverLength(text)

    return frame.save_png()


add_meme(
    "emperor_dragon",
    emperor_dragon,
    min_texts=1,
    max_texts=1,
    keywords=["皇帝龙图"],
    date_created=datetime(2024, 10, 30),
    date_modified=datetime(2024, 10, 30),
)
