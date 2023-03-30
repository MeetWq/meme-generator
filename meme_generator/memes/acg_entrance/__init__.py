from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def acg_entrance(images: List[BuildImage], texts: List[str], args):
    text = texts[0] if texts else "走，跟我去二次元吧"
    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (30, 720, frame.width - 30, 810),
            text,
            max_fontsize=50,
            min_fontsize=25,
            fill="white",
        )
    except ValueError:
        raise TextOverLength(text)

    def make(img: BuildImage) -> BuildImage:
        img = img.convert("RGBA").resize((290, 410), keep_ratio=True)
        return frame.copy().paste(img, (190, 265), below=True)

    return make_jpg_or_gif(images[0], make)


add_meme(
    "acg_entrance",
    acg_entrance,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=["走，跟我去二次元吧"],
    keywords=["二次元入口"],
)
