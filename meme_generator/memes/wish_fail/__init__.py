from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def wish_fail(images, texts: list[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (70, 305, 320, 380),
            text,
            allow_wrap=True,
            max_fontsize=80,
            min_fontsize=20,
        )
    except ValueError:
        raise TextOverLength(text)
    return frame.save_jpg()


add_meme(
    "wish_fail",
    wish_fail,
    min_texts=1,
    max_texts=1,
    default_texts=["我要对象"],
    keywords=["许愿失败"],
    date_created=datetime(2022, 10, 21),
    date_modified=datetime(2023, 2, 14),
)
