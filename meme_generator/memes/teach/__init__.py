from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.tags import MemeTags
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"

default_text = "我老婆"


def teach(images: list[BuildImage], texts: list[str], args):
    frame = BuildImage.open(img_dir / "0.png").resize_width(960).convert("RGBA")
    text = texts[0] if texts else default_text
    try:
        frame.draw_text(
            (10, frame.height - 80, frame.width - 10, frame.height - 5),
            text,
            max_fontsize=50,
            fill="white",
            stroke_fill="black",
            stroke_ratio=0.06,
        )
    except ValueError:
        raise TextOverLength(text)

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize((550, 395), keep_ratio=True)
        return frame.copy().paste(img, (313, 60), below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "teach",
    teach,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=[default_text],
    keywords=["讲课", "敲黑板"],
    tags=MemeTags.takina,
    date_created=datetime(2022, 8, 16),
    date_modified=datetime(2023, 2, 14),
)
