from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"

default_text = "朋友\n先看看这个图标再说话"


def look_this_icon(images: list[BuildImage], texts: list[str], args):
    text = texts[0] if texts else default_text
    frame = BuildImage.open(img_dir / "nmsl.png")
    try:
        frame.draw_text(
            (0, 933, 1170, 1143),
            text,
            lines_align="center",
            font_style="bold",
            max_fontsize=100,
            min_fontsize=50,
        )
    except ValueError:
        raise TextOverLength(text)

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize((515, 515), keep_ratio=True)
        return frame.copy().paste(img, (599, 403), below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "look_this_icon",
    look_this_icon,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=[default_text],
    keywords=["看图标"],
    date_created=datetime(2022, 10, 7),
    date_modified=datetime(2023, 2, 14),
)
