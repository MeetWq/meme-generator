from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def fanatic(images, texts: list[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.jpg")
    try:
        frame.draw_text(
            (145, 40, 343, 160),
            text,
            allow_wrap=True,
            lines_align="center",
            max_fontsize=70,
            min_fontsize=30,
        )
    except ValueError:
        raise TextOverLength(text)
    return frame.save_jpg()


add_meme(
    "fanatic",
    fanatic,
    min_texts=1,
    max_texts=1,
    default_texts=["洛天依"],
    keywords=["狂爱", "狂粉"],
    date_created=datetime(2021, 12, 15),
    date_modified=datetime(2023, 2, 14),
)
