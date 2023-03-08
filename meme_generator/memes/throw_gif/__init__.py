from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def throw_gif(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle()
    locs = [
        [(32, 32, 108, 36)],
        [(32, 32, 122, 36)],
        [],
        [(123, 123, 19, 129)],
        [(185, 185, -50, 200), (33, 33, 289, 70)],
        [(32, 32, 280, 73)],
        [(35, 35, 259, 31)],
        [(175, 175, -50, 220)],
    ]
    frames: List[IMG] = []
    for i in range(8):
        frame = BuildImage.open(img_dir / f"{i}.png")
        for w, h, x, y in locs[i]:
            frame.paste(img.resize((w, h)), (x, y), alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.1)


add_meme("throw_gif", throw_gif, min_images=1, max_images=1, keywords=["抛", "掷"])
