from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def klee_eat(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").square().resize((83, 83))
    # fmt: off
    locs = [
        (0, 174), (0, 174), (0, 174), (0, 174), (0, 174),
        (12, 160), (19, 152), (23, 148), (26, 145), (32, 140),
        (37, 136), (42, 131), (49, 127), (70, 126), (88, 128),
        (-30, 210), (-19, 207), (-14, 200), (-10, 188), (-7, 179),
        (-3, 170), (-3, 175), (-1, 174), (0, 174), (0, 174),
        (0, 174), (0, 174), (0, 174), (0, 174), (0, 174), (0, 174)
    ]
    # fmt: on
    frames: List[IMG] = []
    for i in range(31):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(img, locs[i], below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.1)


add_meme("klee_eat", klee_eat, min_images=1, max_images=1, keywords=["可莉吃"])
