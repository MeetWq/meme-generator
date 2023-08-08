from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength


img_dir = Path(__file__).parent / "images"


def shiori(images, texts: List[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (2, 160, frame.width - 2, frame.height - 2),
            text,
            allow_wrap=True,
            lines_align="center",
            max_fontsize=20,
            min_fontsize=10,
            fill=(0, 0, 0),
            stroke_ratio=1 / 15,
            stroke_fill="white",
        )
    except ValueError:
        raise TextOverLength(text)
    return frame.save_png()


add_meme(
    "shiori",
    shiori,
    min_texts=1,
    max_texts=1,
    default_texts=["让我栞栞"],
    keywords=["栞栞"],
)
