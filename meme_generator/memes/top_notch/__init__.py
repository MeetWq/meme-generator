from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def top_notch(images, texts: list[str], args):
    frame = BuildImage.open(img_dir / "0.png")
    text = f"好，不愧是顶尖{texts[0]}"
    try:
        frame.draw_text(
            (10, 240, 420, 300),
            text,
            allow_wrap=True,
            max_fontsize=40,
            min_fontsize=20,
        )
    except ValueError:
        raise TextOverLength(texts[0])
    return frame.save_png()


add_meme(
    "top_notch",
    top_notch,
    min_texts=1,
    max_texts=1,
    default_texts=["运营"],
    keywords=["顶尖"],
    date_created=datetime(2024, 8, 17),
    date_modified=datetime(2024, 8, 17),
)
