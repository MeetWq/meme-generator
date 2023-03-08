from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def bad_news(images, texts: List[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (50, 100, frame.width - 50, frame.height - 100),
            text,
            allow_wrap=True,
            lines_align="center",
            max_fontsize=60,
            min_fontsize=30,
            fill=(0, 0, 0),
            stroke_ratio=1 / 15,
            stroke_fill="white",
        )
    except ValueError:
        raise TextOverLength(text)
    return frame.save_png()


add_meme(
    "bad_news",
    bad_news,
    min_texts=1,
    max_texts=1,
    default_texts=["喜报"],
    keywords=["悲报"],
)
