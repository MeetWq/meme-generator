from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def back_to_work(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")
    img = (
        images[0].convert("RGBA").resize((220, 310), keep_ratio=True, direction="north")
    )
    frame.paste(img.rotate(25, expand=True), (56, 32), below=True)
    return frame.save_jpg()


add_meme(
    "back_to_work",
    back_to_work,
    min_images=1,
    max_images=1,
    keywords=["继续干活", "打工人"],
    date_created=datetime(2022, 3, 10),
    date_modified=datetime(2023, 2, 14),
)
