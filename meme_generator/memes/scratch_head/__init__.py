from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def scratch_head(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").square().resize((68, 68))
    frames: list[IMG] = []
    locs = [
        (53, 46, 4, 5),
        (50, 45, 7, 6),
        (50, 42, 6, 8),
        (50, 44, 7, 7),
        (53, 42, 4, 8),
        (52, 45, 7, 7),
    ]
    for i in range(6):
        frame = BuildImage.open(img_dir / f"{i}.png")
        w, h, x, y = locs[i]
        frame.paste(img.resize((w, h)), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.1)


add_meme(
    "scratch_head",
    scratch_head,
    min_images=1,
    max_images=1,
    keywords=["挠头"],
    date_created=datetime(2023, 1, 7),
    date_modified=datetime(2023, 2, 14),
)
