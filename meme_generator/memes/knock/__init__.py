from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def knock(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").square()
    # fmt: off
    locs = [(60, 308, 210, 195), (60, 308, 210, 198), (45, 330, 250, 172), (58, 320, 218, 180),
            (60, 310, 215, 193), (40, 320, 250, 285), (48, 308, 226, 192), (51, 301, 223, 200)]
    # fmt: on
    frames: list[IMG] = []
    for i in range(8):
        frame = BuildImage.open(img_dir / f"{i}.png")
        x, y, w, h = locs[i]
        frame.paste(img.resize((w, h)), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.04)


add_meme(
    "knock",
    knock,
    min_images=1,
    max_images=1,
    keywords=["敲"],
    tags=MemeTags.gura,
    date_created=datetime(2022, 4, 14),
    date_modified=datetime(2023, 2, 14),
)
