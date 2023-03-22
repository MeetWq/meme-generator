from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def look_this_icon(images: List[BuildImage], texts: List[str], args):
    text = texts[0] if texts else "朋友\n先看看这个图标再说话"
    frame = BuildImage.open(img_dir / "nmsl.png")
    try:
        frame.draw_text(
            (0, 933, 1170, 1143),
            text,
            lines_align="center",
            weight="bold",
            max_fontsize=100,
            min_fontsize=50,
        )
    except ValueError:
        raise TextOverLength(text)

    def make(img: BuildImage) -> BuildImage:
        img = img.convert("RGBA").resize((515, 515), keep_ratio=True)
        return frame.copy().paste(img, (599, 403), below=True)

    return make_jpg_or_gif(images[0], make)


add_meme(
    "look_this_icon",
    look_this_icon,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=["朋友\n先看看这个图标再说话"],
    keywords=["看图标"],
)
