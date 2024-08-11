from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def capoo_rub(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").square().resize((180, 180))
    frames: list[IMG] = []
    locs = [
        (178, 184, 78, 260),
        (178, 174, 84, 269),
        (178, 174, 84, 269),
        (178, 178, 84, 264),
    ]
    for i in range(4):
        frame = BuildImage.open(img_dir / f"{i}.png")
        w, h, x, y = locs[i]
        frame.paste(img.resize((w, h)), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.1)


add_meme(
    "capoo_rub",
    capoo_rub,
    min_images=1,
    max_images=1,
    keywords=["咖波蹭", "咖波贴"],
    tags=MemeTags.capoo,
    date_created=datetime(2022, 11, 29),
    date_modified=datetime(2023, 2, 14),
)
