from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def not_call_me(images, texts: List[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (228, 11, 340, 164),
            text,
            allow_wrap=True,
            max_fontsize=80,
            min_fontsize=20,
        )
    except ValueError:
        raise TextOverLength(text)
    return frame.save_png()


add_meme(
    "not_call_me",
    not_call_me,
    min_texts=1,
    max_texts=1,
    default_texts=["开银趴不喊我是吧"],
    keywords=["不喊我"],
)
