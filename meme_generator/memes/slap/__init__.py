from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def slap(images, texts: List[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.jpg")
    try:
        frame.draw_text(
            (20, 450, 620, 630),
            text,
            allow_wrap=True,
            max_fontsize=110,
            min_fontsize=50,
        )
    except ValueError:
        raise TextOverLength(text)
    return frame.save_jpg()


add_meme("slap", slap, min_texts=1, max_texts=1, keywords=["一巴掌"])
