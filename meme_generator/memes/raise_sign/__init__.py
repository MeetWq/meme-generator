from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def raise_sign(images, texts: List[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.jpg")
    text_img = BuildImage.new("RGBA", (360, 260))
    try:
        text_img.draw_text(
            (10, 10, 350, 250),
            text,
            max_fontsize=80,
            min_fontsize=30,
            allow_wrap=True,
            lines_align="center",
            spacing=10,
            fontname="FZShaoEr-M11S",
            fill="#51201b",
        )
    except ValueError:
        raise TextOverLength(text)
    text_img = text_img.perspective(((33, 0), (375, 120), (333, 387), (0, 258)))
    frame.paste(text_img, (285, 24), alpha=True)
    return frame.save_jpg()


add_meme(
    "raise_sign",
    raise_sign,
    min_texts=1,
    max_texts=1,
    default_texts=["大佬带带我"],
    keywords=["举牌"],
)
