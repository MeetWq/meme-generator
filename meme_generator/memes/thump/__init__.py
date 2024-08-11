from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def thump(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").square()
    # fmt: off
    locs = [(65, 128, 77, 72), (67, 128, 73, 72), (54, 139, 94, 61), (57, 135, 86, 65)]
    # fmt: on
    frames: list[IMG] = []
    for i in range(4):
        frame = BuildImage.open(img_dir / f"{i}.png")
        x, y, w, h = locs[i]
        frame.paste(img.resize((w, h)), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.04)


add_meme(
    "thump",
    thump,
    min_images=1,
    max_images=1,
    keywords=["捶"],
    date_created=datetime(2022, 3, 30),
    date_modified=datetime(2023, 2, 14),
)
