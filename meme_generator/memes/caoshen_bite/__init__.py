from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def caoshen_bite(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").resize((160, 140), keep_ratio=True)
    # fmt: off
    locs = [
        (123, 356, 158, 124), (123, 356, 158, 124), (123, 355, 158, 125),
        (122, 352, 159, 128), (122, 350, 159, 130), (122, 348, 159, 132),
        (122, 345, 159, 135), (121, 343, 160, 137), (121, 342, 160, 138),
        (121, 341, 160, 139), (121, 341, 160, 139), (121, 342, 160, 138),
        (121, 344, 160, 136), (121, 346, 160, 134), (122, 349, 159, 131),
        (122, 351, 159, 129), (122, 353, 159, 127), (123, 355, 158, 125),
    ]
    # fmt: on
    frames: List[IMG] = []
    for i in range(38):
        frame = BuildImage.open(img_dir / f"{i}.png")
        x, y, w, h = locs[i % len(locs)]
        frame.paste(img.resize((w, h)), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.1)


add_meme("caoshen_bite", caoshen_bite, min_images=1, max_images=1, keywords=["草神啃"])
