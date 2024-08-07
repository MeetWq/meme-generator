from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def twist(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").square().resize((78, 78))
    # fmt: off
    locs = [
        (25, 66, 0), (25, 66, 60), (23, 68, 120),
        (20, 69, 180), (22, 68, 240), (25, 66, 300)
    ]
    # fmt: on
    frames: list[IMG] = []
    for i in range(5):
        frame = BuildImage.open(img_dir / f"{i}.png")
        x, y, a = locs[i]
        frame.paste(img.rotate(a), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.1)


add_meme(
    "twist",
    twist,
    min_images=1,
    max_images=1,
    keywords=["搓"],
    date_created=datetime(2022, 3, 9),
    date_modified=datetime(2023, 2, 14),
)
