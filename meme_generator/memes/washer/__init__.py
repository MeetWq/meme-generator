from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def washer(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA")
    frame = BuildImage.open(img_dir / "0.png")
    frames: list[IMG] = []
    for i in range(0, 360, 30):
        frames.append(
            frame.copy()
            .paste(img.rotate(-i).resize((74, 74)), (63, 56), below=True)
            .image
        )
    return save_gif(frames, 0.1)


add_meme(
    "washer",
    washer,
    min_images=1,
    max_images=1,
    keywords=["洗衣机"],
    date_created=datetime(2024, 1, 18),
    date_modified=datetime(2024, 1, 18),
)
