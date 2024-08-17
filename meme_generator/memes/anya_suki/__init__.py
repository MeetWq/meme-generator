from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.tags import MemeTags
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"

default_text = "阿尼亚喜欢这个"


def anya_suki(images: list[BuildImage], texts: list[str], args):
    text = texts[0] if texts else default_text
    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (5, frame.height - 60, frame.width - 5, frame.height - 10),
            text,
            max_fontsize=40,
            fill="white",
            stroke_fill="black",
            stroke_ratio=0.06,
        )
    except ValueError:
        raise TextOverLength(text)

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize((305, 235), keep_ratio=True)
        return frame.copy().paste(img, (106, 72), below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "anya_suki",
    anya_suki,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=[default_text],
    keywords=["阿尼亚喜欢"],
    tags=MemeTags.anya,
    date_created=datetime(2022, 5, 10),
    date_modified=datetime(2023, 2, 14),
)
