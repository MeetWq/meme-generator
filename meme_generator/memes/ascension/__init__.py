from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def ascension(images, texts: List[str], args):
    frame = BuildImage.open(img_dir / "0.png")
    text = f"你原本应该要去地狱的，但因为你生前{texts[0]}，我们就当作你已经服完刑期了"
    try:
        frame.draw_text(
            (40, 30, 482, 135),
            text,
            allow_wrap=True,
            max_fontsize=50,
            min_fontsize=20,
        )
    except ValueError:
        raise TextOverLength(texts[0])
    return frame.save_jpg()


add_meme(
    "ascension",
    ascension,
    min_texts=1,
    max_texts=1,
    default_texts=["学的是机械"],
    keywords=["升天"],
)
