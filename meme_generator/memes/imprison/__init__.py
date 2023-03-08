from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def imprison(images, texts: List[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.jpg")
    try:
        frame.draw_text(
            (10, 157, 230, 197),
            text,
            allow_wrap=True,
            max_fontsize=35,
            min_fontsize=15,
        )
    except ValueError:
        raise TextOverLength(text)
    return frame.save_jpg()


add_meme(
    "imprison",
    imprison,
    min_texts=1,
    max_texts=1,
    default_texts=["我发涩图被抓起来了"],
    keywords=["坐牢"],
)
