from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.tags import MemeTags

img_dir = Path(__file__).parent / "images"


def nekoha_holdsign(images, texts: list[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.jpg")
    try:
        frame.draw_text(
            (210, 520, 570, 765),
            text,
            fill=(72, 110, 173),
            allow_wrap=True,
            font_families=["FZShaoEr-M11S"],
            max_fontsize=65,
            min_fontsize=25,
            lines_align="center",
        )
    except ValueError:
        raise TextOverLength(text)
    return frame.save_jpg()


add_meme(
    "nekoha_holdsign",
    nekoha_holdsign,
    min_texts=1,
    max_texts=1,
    default_texts=["V我50"],
    keywords=["猫羽雫举牌", "猫猫举牌"],
    tags=MemeTags.nekoha,
    date_created=datetime(2023, 3, 30),
    date_modified=datetime(2023, 3, 30),
)
