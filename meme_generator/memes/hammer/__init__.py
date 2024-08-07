from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def hammer(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").square()
    # fmt: off
    locs = [
        (62, 143, 158, 113), (52, 177, 173, 105), (42, 192, 192, 92), (46, 182, 184, 100),
        (54, 169, 174, 110), (69, 128, 144, 135), (65, 130, 152, 124),
    ]
    # fmt: on
    frames: list[IMG] = []
    for i in range(7):
        frame = BuildImage.open(img_dir / f"{i}.png")
        x, y, w, h = locs[i]
        frame.paste(img.resize((w, h)), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.07)


add_meme(
    "hammer",
    hammer,
    min_images=1,
    max_images=1,
    keywords=["锤"],
    date_created=datetime(2022, 4, 20),
    date_modified=datetime(2023, 2, 14),
)
