from datetime import datetime
from pathlib import Path

from meme_generator import add_meme
from meme_generator.utils import save_gif
from PIL.Image import Image as IMG
from pil_utils import BuildImage

img_dir = Path(__file__).parent / "images"


def behead(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").square().resize((75, 75))
    # fmt: off
    locs = [
        (80, 72, 0), (83, 73, 0), (82, 73, 0),
        (78, 73, 0), (72, 74, 0), (72, 75, 0),
        (73, 76, 0), (73, 76, 0), (73, 76, 0),
        (74, 76, 0), (74, 76, 0), (70, 73, 12),
        (61, 62, 25), (49, 40, 45), (46, 30, 65),
        (50, 35, 85), (39, 34, 105), (19, 45, 135),
        (9, 91, 155), (6, 161, 175), (-4, 248, 180),
    ]
    # fmt: on
    frames: list[IMG] = []
    for i in range(21):
        frame = BuildImage.open(img_dir / f"{i}.png")
        x, y, angle = locs[i]
        frame.paste(img.rotate(angle, expand=True), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.05)


add_meme(
    "behead",
    behead,
    min_images=1,
    max_images=1,
    keywords=["砍头", "斩首"],
    date_created=datetime(2023, 7, 1),
    date_modified=datetime(2023, 7, 1),
)
