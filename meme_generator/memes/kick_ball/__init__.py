from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def kick_ball(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").square().resize((78, 78))
    # fmt: off
    locs = [
        (57, 136), (56, 117), (55, 99), (52, 113), (50, 126),
        (48, 139), (47, 112), (47, 85), (47, 57), (48, 97),
        (50, 136), (51, 176), (52, 169), (55, 181), (58, 153)
    ]
    # fmt: on
    frames: List[IMG] = []
    for i in range(15):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(img.rotate(-24 * i), locs[i], below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.1)


add_meme("kick_ball", kick_ball, min_images=1, max_images=1, keywords=["踢球"])
