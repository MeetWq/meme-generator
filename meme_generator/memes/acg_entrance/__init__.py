from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"

default_text = "走，跟我去二次元吧"


def acg_entrance(images: list[BuildImage], texts: list[str], args):
    text = texts[0] if texts else default_text
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

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize((290, 410), keep_ratio=True)
        return frame.copy().paste(img, (190, 265), below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "acg_entrance",
    acg_entrance,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=[default_text],
    keywords=["二次元入口"],
    date_created=datetime(2023, 3, 30),
    date_modified=datetime(2023, 3, 30),
)
