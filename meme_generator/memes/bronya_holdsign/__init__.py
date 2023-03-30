from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def bronya_holdsign(images, texts: List[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.jpg")
    try:
        frame.draw_text(
            (190, 675, 640, 930),
            text,
            fill=(111, 95, 95),
            allow_wrap=True,
            max_fontsize=60,
            min_fontsize=25,
            lines_align="center",
        )
    except ValueError:
        raise TextOverLength(text)
    return frame.save_jpg()


add_meme(
    "bronya_holdsign",
    bronya_holdsign,
    min_texts=1,
    max_texts=1,
    default_texts=["V我50"],
    keywords=["布洛妮娅举牌", "大鸭鸭举牌"],
)
