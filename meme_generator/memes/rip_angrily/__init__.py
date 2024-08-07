from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def rip_angrily(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").square().resize((105, 105))
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img.rotate(-24, expand=True), (18, 170), below=True)
    frame.paste(img.rotate(24, expand=True), (163, 65), below=True)
    return frame.save_jpg()


add_meme(
    "rip_angrily",
    rip_angrily,
    min_images=1,
    max_images=1,
    keywords=["怒撕"],
    date_created=datetime(2022, 10, 9),
    date_modified=datetime(2023, 2, 14),
)
