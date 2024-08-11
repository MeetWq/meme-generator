from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def potato(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")
    img = images[0].convert("RGBA").square().resize((458, 458))
    frame.paste(img.rotate(-5), (531, 15), below=True)
    return frame.save_jpg()


add_meme(
    "potato",
    potato,
    min_images=1,
    max_images=1,
    keywords=["土豆"],
    date_created=datetime(2023, 1, 19),
    date_modified=datetime(2023, 2, 14),
)
