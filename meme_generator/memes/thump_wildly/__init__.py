from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def thump_wildly(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").resize((122, 122), keep_ratio=True)
    raw_frames = [BuildImage.open(img_dir / f"{i}.png") for i in range(31)]
    for i in range(14):
        raw_frames[i].paste(img, (203, 196), below=True)
    raw_frames[14].paste(img, (207, 239), below=True)
    frames = [frame.image for frame in raw_frames]
    for i in range(6):
        frames.append(frames[0])
    return save_gif(frames, 0.04)


add_meme(
    "thump_wildly", thump_wildly, min_images=1, max_images=1, keywords=["捶爆", "爆捶"]
)
