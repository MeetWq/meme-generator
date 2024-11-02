from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"

default_text = "平安名すみれ"


def police(images: list[BuildImage], texts: list[str], args):
    text = default_text if not texts else texts[0]
    text_frame = BuildImage.new("RGBA", (250, 85))
    try:
        text_frame.draw_text(
            (0, 0, 250, 85),
            text,
            font_families=["Noto Serif SC"],
            max_fontsize=60,
            min_fontsize=20,
        )
    except ValueError:
        raise TextOverLength(text)
    img = images[0].convert("RGBA").square().resize((245, 245))

    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img, (224, 46), below=True)
    frame.paste(text_frame, (220, 395), alpha=True)
    return frame.save_jpg()


def police1(images: list[BuildImage], texts, args):
    img = (
        images[0]
        .convert("RGBA")
        .resize((60, 75), keep_ratio=True)
        .rotate(16, expand=True)
    )
    frame = BuildImage.open(img_dir / "1.png")
    frame.paste(img, (37, 291), below=True)
    return frame.save_jpg()


add_meme(
    "police",
    police,
    min_images=1,
    max_images=1,
    max_texts=1,
    min_texts=0,
    default_texts=[default_text],
    keywords=["出警"],
    date_created=datetime(2022, 2, 23),
    date_modified=datetime(2024, 9, 6),
)

add_meme(
    "police1",
    police1,
    min_images=1,
    max_images=1,
    keywords=["警察"],
    date_created=datetime(2022, 3, 12),
    date_modified=datetime(2023, 2, 14),
)
