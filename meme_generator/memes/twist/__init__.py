from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def twist(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").square().resize((78, 78))
    # fmt: off
    locs = [
        (25, 66, 0), (25, 66, 60), (23, 68, 120),
        (20, 69, 180), (22, 68, 240), (25, 66, 300)
    ]
    # fmt: on
    frames: List[IMG] = []
    for i in range(5):
        frame = BuildImage.open(img_dir / f"{i}.png")
        x, y, a = locs[i]
        frame.paste(img.rotate(a), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.1)


add_meme("twist", twist, min_images=1, max_images=1, keywords=["搓"])
