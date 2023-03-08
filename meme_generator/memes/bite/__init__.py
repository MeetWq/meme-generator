from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def bite(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").square()
    frames: List[IMG] = []
    # fmt: off
    locs = [
        (90, 90, 105, 150), (90, 83, 96, 172), (90, 90, 106, 148),
        (88, 88, 97, 167), (90, 85, 89, 179), (90, 90, 106, 151)
    ]
    # fmt: on
    for i in range(6):
        frame = BuildImage.open(img_dir / f"{i}.png")
        w, h, x, y = locs[i]
        frame.paste(img.resize((w, h)), (x, y), below=True)
        frames.append(frame.image)
    for i in range(6, 16):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frames.append(frame.image)
    return save_gif(frames, 0.07)


add_meme("bite", bite, min_images=1, max_images=1, keywords=["啃"])
