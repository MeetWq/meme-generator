from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"

default_text = "说完了吗？该走了"


def time_to_go(images: list[BuildImage], texts: list[str], args):
    img = images[0].resize((105, 105), keep_ratio=True)
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img, (230, 82), below=True)
    text = texts[0] if texts else default_text
    try:
        frame.draw_text(
            (20, 232, 330, 312),
            text,
            min_fontsize=20,
            max_fontsize=40,
            fill="black",
        )
    except ValueError:
        raise TextOverLength(text)
    return frame.save_jpg()


add_meme(
    "time_to_go",
    time_to_go,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=[default_text],
    keywords=["该走了"],
    date_created=datetime(2024, 9, 4),
    date_modified=datetime(2024, 9, 4),
)
