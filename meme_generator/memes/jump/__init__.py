from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def jump(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle().resize((40, 40))
    locs = [
        (15, 50),
        (13, 43),
        (15, 23),
        (14, 4),
        (16, -3),
        (16, -4),
        (14, 4),
        (15, 31),
    ]
    frames: list[IMG] = []
    for i in range(8):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(img, locs[i], alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.05)


add_meme(
    "jump",
    jump,
    min_images=1,
    max_images=1,
    keywords=["跳"],
    date_created=datetime(2024, 7, 14),
    date_modified=datetime(2024, 7, 14),
)
