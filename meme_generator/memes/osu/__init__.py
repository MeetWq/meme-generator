from io import BytesIO
from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def osu(images, texts: List[str], args) -> BytesIO:
    text = texts[0]
    frame = BuildImage.open(img_dir / "osu.png")
    try:
        frame.draw_text(
            (80, 80, 432, 432),
            text,
            max_fontsize=192,
            min_fontsize=80,
            weight="bold",
            fill="white",
            lines_align="center",
            fontname="Aller",
        )
    except ValueError:
        raise TextOverLength(text)

    return frame.save_png()


add_meme(
    "osu",
    osu,
    min_texts=1,
    max_texts=1,
    default_texts=["hso!"],
    keywords=["osu"],
)
