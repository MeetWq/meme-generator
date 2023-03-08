from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def scratchcard(images, texts: List[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (80, 160, 360, 290),
            text,
            allow_wrap=True,
            max_fontsize=80,
            min_fontsize=30,
            fill="white",
            lines_align="center",
        )
    except ValueError:
        raise TextOverLength(text)
    mask = BuildImage.open(img_dir / "1.png")
    frame.paste(mask, alpha=True)
    return frame.save_jpg()


add_meme(
    "scratchcard",
    scratchcard,
    min_texts=1,
    max_texts=1,
    default_texts=["谢谢参与"],
    keywords=["刮刮乐"],
)
