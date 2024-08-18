from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import CommandShortcut, add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def wakeup(images, texts: list[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.jpg")
    try:
        frame.draw_text((310, 270, 460, 380), text, max_fontsize=90, min_fontsize=50)
    except ValueError:
        raise TextOverLength(text)
    frame.draw_text(
        (50, 610, 670, 720), f"{text}起来了", max_fontsize=110, min_fontsize=70
    )
    return frame.save_jpg()


add_meme(
    "wakeup",
    wakeup,
    min_texts=1,
    max_texts=1,
    default_texts=["好"],
    keywords=["好起来了"],
    shortcuts=[
        CommandShortcut(
            key=r"(?P<text>\S{1,4})\s+起来了",
            args=["{text}"],
            humanized="xx 起来了",
        )
    ],
    date_created=datetime(2022, 6, 12),
    date_modified=datetime(2023, 2, 14),
)
