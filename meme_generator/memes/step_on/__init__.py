from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def step_on(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").resize((100, 100), keep_ratio=True)
    frames: list[IMG] = []
    locs = [
        (104, 72, 32, 185, -25),
        (104, 72, 32, 185, -25),
        (90, 73, 51, 207, 0),
        (88, 78, 51, 202, 0),
        (88, 86, 49, 197, 0),
    ]
    for i in range(5):
        frame = BuildImage.open(img_dir / f"{i}.png")
        w, h, x, y, angle = locs[i]
        frame.paste(img.resize((w, h)).rotate(angle, expand=True), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.07)


add_meme(
    "step_on",
    step_on,
    min_images=1,
    max_images=1,
    keywords=["踩"],
    date_created=datetime(2023, 3, 28),
    date_modified=datetime(2023, 3, 28),
)
