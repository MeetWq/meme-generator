from typing import List
from pathlib import Path
from pil_utils import BuildImage
from PIL.Image import Image as IMG

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import save_gif, make_jpg_or_gif, make_gif_or_combined_gif


img_dir = Path(__file__).parent / "images"


def slap(images, texts: List[str], args):
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
        return OVER_LENGTH_MSG
    return frame.save_jpg()

add_meme("slap", ['一巴掌'], slap, min_texts=1, max_texts=1)
