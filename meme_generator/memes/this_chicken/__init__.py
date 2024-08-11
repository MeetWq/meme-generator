from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"

default_text = "这是十二生肖中的鸡"


def this_chicken(images: list[BuildImage], texts, args):
    text = texts[0] if texts else default_text
    img = images[0].convert("RGBA").resize((640, 640), keep_ratio=True)

    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (0, 900, 1440, 1080),
            text,
            max_fontsize=80,
            min_fontsize=40,
            fill="white",
            stroke_ratio=1 / 15,
            stroke_fill="black",
        )
    except ValueError:
        raise TextOverLength(text)
    frame.paste(
        img.perspective(((507, 0), (940, 351), (383, 625), (0, 256))),
        (201, 201),
        below=True,
    )
    return frame.save_jpg()


add_meme(
    "this_chicken",
    this_chicken,
    min_images=1,
    max_images=1,
    max_texts=1,
    default_texts=[default_text],
    keywords=["这是鸡", "🐔"],
    date_created=datetime(2023, 11, 12),
    date_modified=datetime(2024, 1, 18),
)
