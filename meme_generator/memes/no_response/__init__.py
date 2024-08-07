from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def no_response(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").resize((1050, 783), keep_ratio=True)
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img, (0, 581), below=True)
    return frame.save_jpg()


add_meme(
    "no_response",
    no_response,
    min_images=1,
    max_images=1,
    keywords=["无响应"],
    date_created=datetime(2022, 10, 1),
    date_modified=datetime(2023, 2, 14),
)
