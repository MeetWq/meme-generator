from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.tags import MemeTags
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"

default_text = "所谓的男人啊，只要送他们这种东西就会很开心"


def frieren_take(images: list[BuildImage], texts: list[str], args):
    frame = BuildImage.open(img_dir / "0.png")
    text = texts[0] if texts else default_text
    try:
        frame.draw_text(
            (100, frame.height - 120, frame.width - 100, frame.height),
            text,
            max_fontsize=50,
            min_fontsize=20,
            fill="white",
            stroke_fill="black",
            stroke_ratio=0.05,
        )
    except ValueError:
        raise TextOverLength(text)

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize((102, 108), keep_ratio=True)
        return frame.copy().paste(img, (130, 197), below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "frieren_take",
    frieren_take,
    min_images=1,
    max_images=1,
    max_texts=1,
    default_texts=[default_text],
    keywords=["芙莉莲拿"],
    tags=MemeTags.frieren,
    date_created=datetime(2024, 1, 18),
    date_modified=datetime(2024, 8, 9),
)
