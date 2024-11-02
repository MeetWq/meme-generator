from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import CommandShortcut, add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def intel_inside(images, texts: list[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.jpg")
    try:
        frame.draw_text(
            (240, 340, 680, 580),
            text,
            allow_wrap=False,
            max_fontsize=180,
            min_fontsize=80,
            fill="white",
            font_families=["Neo Sans"],
            font_style="bold",
        )
    except ValueError:
        raise TextOverLength(text)
    return frame.save_jpg()


add_meme(
    "intel_inside",
    intel_inside,
    min_texts=1,
    max_texts=1,
    default_texts=["intel"],
    keywords=["inside"],
    shortcuts=[
        CommandShortcut(
            key=r"(?P<text>\S{1,10})\s+inside",
            args=["{text}"],
            humanized="xx inside",
        ),
    ],
    date_created=datetime(2024, 10, 29),
    date_modified=datetime(2024, 10, 29),
)
