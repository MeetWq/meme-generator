from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def nijika_holdsign(images, texts: List[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.jpg")
    try:
        frame.draw_text(
            (57, 279, 249, 405),
            text,
            fill=(111, 95, 95),
            allow_wrap=True,
            max_fontsize=60,
            min_fontsize=25,
            lines_align="center",
            fontname="FZSJ-QINGCRJ",
        )
    except ValueError:
        raise TextOverLength(text)
    return frame.save_jpg()


add_meme(
    "nijika_holdsign",
    nijika_holdsign,
    min_texts=1,
    max_texts=1,
    default_texts=["你可少看点二次元吧"],
    keywords=["伊地知虹夏举牌", "虹夏举牌"],
)
