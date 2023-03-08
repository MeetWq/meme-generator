from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def roll(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").square().resize((210, 210))
    # fmt: off
    locs = [
        (87, 77, 0), (96, 85, -45), (92, 79, -90), (92, 78, -135),
        (92, 75, -180), (92, 75, -225), (93, 76, -270), (90, 80, -315)
    ]
    # fmt: on
    frames: List[IMG] = []
    for i in range(8):
        frame = BuildImage.open(img_dir / f"{i}.png")
        x, y, a = locs[i]
        frame.paste(img.rotate(a), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.1)


add_meme("roll", roll, min_images=1, max_images=1, keywords=["滚"])
