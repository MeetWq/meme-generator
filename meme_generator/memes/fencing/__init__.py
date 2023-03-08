from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def fencing(images: List[BuildImage], texts, args):
    self_head = images[0].convert("RGBA").circle().resize((27, 27))
    user_head = images[1].convert("RGBA").circle().resize((27, 27))
    # fmt: off
    user_locs = [
        (57, 4), (55, 5), (58, 7), (57, 5), (53, 8), (54, 9),
        (64, 5), (66, 8), (70, 9), (73, 8), (81, 10), (77, 10),
        (72, 4), (79, 8), (50, 8), (60, 7), (67, 6), (60, 6), (50, 9)
    ]
    self_locs = [
        (10, 6), (3, 6), (32, 7), (22, 7), (13, 4), (21, 6),
        (30, 6), (22, 2), (22, 3), (26, 8), (23, 8), (27, 10),
        (30, 9), (17, 6), (12, 8), (11, 7), (8, 6), (-2, 10), (4, 9)
    ]
    # fmt: on
    frames: List[IMG] = []
    for i in range(19):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(user_head, user_locs[i], alpha=True)
        frame.paste(self_head, self_locs[i], alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.05)


add_meme("fencing", fencing, min_images=2, max_images=2, keywords=["击剑", "🤺"])
