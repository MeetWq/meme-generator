from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def hug_leg(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").square()
    locs = [
        (50, 73, 68, 92),
        (58, 60, 62, 95),
        (65, 10, 67, 118),
        (61, 20, 77, 97),
        (55, 44, 65, 106),
        (66, 85, 60, 98),
    ]
    frames: list[IMG] = []
    for i in range(6):
        frame = BuildImage.open(img_dir / f"{i}.png")
        x, y, w, h = locs[i]
        frame.paste(img.resize((w, h)), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.06)


add_meme(
    "hug_leg",
    hug_leg,
    min_images=1,
    max_images=1,
    keywords=["抱大腿"],
    date_created=datetime(2022, 10, 1),
    date_modified=datetime(2023, 2, 14),
)
