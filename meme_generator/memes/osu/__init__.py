from datetime import datetime
from io import BytesIO
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def osu(images, texts: list[str], args) -> BytesIO:
    text = texts[0]
    frame = BuildImage.open(img_dir / "osu.png")
    try:
        frame.draw_text(
            (80, 80, 432, 432),
            text,
            max_fontsize=192,
            min_fontsize=80,
            font_style="bold",
            fill="white",
            lines_align="center",
            font_families=["Aller"],
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
    date_created=datetime(2023, 7, 27),
    date_modified=datetime(2023, 7, 27),
)
