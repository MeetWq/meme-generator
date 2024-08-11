from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def applaud(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").square().resize((110, 110))
    frames: list[IMG] = []
    locs = [
        (109, 102, 27, 17),
        (107, 105, 28, 15),
        (110, 106, 27, 14),
        (109, 106, 27, 14),
        (107, 108, 29, 12),
    ]
    for i in range(5):
        frame = BuildImage.open(img_dir / f"{i}.png")
        w, h, x, y = locs[i]
        frame.paste(img.resize((w, h)), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.1)


add_meme(
    "applaud",
    applaud,
    min_images=1,
    max_images=1,
    keywords=["鼓掌"],
    date_created=datetime(2023, 1, 8),
    date_modified=datetime(2023, 2, 14),
)
