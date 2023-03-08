from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def shutup(images, texts: List[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.jpg")
    try:
        frame.draw_text(
            (10, 180, 230, 230),
            text,
            allow_wrap=True,
            max_fontsize=40,
            min_fontsize=15,
        )
    except ValueError:
        raise TextOverLength(text)
    return frame.save_jpg()


add_meme(
    "shutup",
    shutup,
    min_texts=1,
    max_texts=1,
    default_texts=["你不要再说了"],
    keywords=["别说了"],
)
