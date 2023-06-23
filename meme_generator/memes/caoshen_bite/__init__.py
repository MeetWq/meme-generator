from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def caoshen_bite(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").square()
    # fmt: off
    locs = [
        (120, 353, 162, 127), (124, 355, 160, 125), (121, 353, 163, 127), (124, 353, 161, 127),
        (122, 353, 164, 127), (122, 350, 161, 130), (122, 349, 160, 131), (121, 341, 162, 139),
        (122, 345, 160, 135), (119, 344, 163, 136), (120, 339, 164, 141), (121, 338, 162, 142),
        (123, 342, 158 ,138), (122, 346, 160, 134), (123, 346, 159, 134), (123, 349, 158, 131),
        (121, 350, 162, 130), (124, 351, 158, 129), (124, 355, 160, 125), (122, 357, 160, 123),
        (123, 351, 156, 129), (122, 351, 158, 129), (122, 353, 160, 127), (121, 350, 162, 130),
        (122, 348, 160, 132), (123, 345, 158, 135), (121, 344, 161, 136), (120, 340, 163, 140),
        (121, 341, 162, 139), (122, 343, 160, 137), (123, 340, 159, 140), (122, 346, 160, 134),
        (123, 344, 159, 136), (122, 351, 160, 129), (123, 351, 159, 129), (123, 352, 159, 128),
        (122, 353, 161, 127), (121, 352, 161, 128),
    ]
    # fmt: on
    frames: List[IMG] = []
    for i in range(38):
        frame = BuildImage.open(img_dir / f"{i}.png")
        x, y, w, h = locs[i]
        frame.paste(img.resize((w, h)), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.1)


add_meme("caoshen_bite", caoshen_bite, min_images=1, max_images=1, keywords=["草神啃"])
