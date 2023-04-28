from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def capoo_draw(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").resize((175, 120), keep_ratio=True)
    params = (
        (((27, 0), (207, 12), (179, 142), (0, 117)), (30, 16)),
        (((28, 0), (207, 13), (180, 137), (0, 117)), (34, 17)),
    )
    raw_frames = [BuildImage.open(img_dir / f"{i}.png") for i in range(6)]
    for i in range(2):
        points, pos = params[i]
        raw_frames[4 + i].paste(img.perspective(points), pos, below=True)

    frames: List[IMG] = []
    frames.append(raw_frames[0].image)
    for i in range(4):
        frames.append(raw_frames[1].image)
        frames.append(raw_frames[2].image)
    frames.append(raw_frames[3].image)
    for i in range(6):
        frames.append(raw_frames[4].image)
        frames.append(raw_frames[5].image)

    return save_gif(frames, 0.1)


add_meme(
    "capoo_draw",
    capoo_draw,
    min_images=1,
    max_images=1,
    keywords=["咖波画"],
)
