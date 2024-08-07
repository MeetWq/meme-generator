from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def support(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").square().resize((815, 815)).rotate(23, expand=True)
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img, (-172, -17), below=True)
    return frame.save_jpg()


add_meme(
    "support",
    support,
    min_images=1,
    max_images=1,
    keywords=["精神支柱"],
    date_created=datetime(2021, 5, 5),
    date_modified=datetime(2023, 2, 14),
)
