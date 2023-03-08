from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def garbage(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").square().resize((79, 79))
    # fmt: off
    locs = (
        [] + [(39, 40)] * 3 + [(39, 30)] * 2 + [(39, 32)] * 10
        + [(39, 30), (39, 27), (39, 32), (37, 49), (37, 64),
           (37, 67), (37, 67), (39, 69), (37, 70), (37, 70)]
    )
    # fmt: on
    frames: List[IMG] = []
    for i in range(25):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(img, locs[i], below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.04)


add_meme("garbage", garbage, min_images=1, max_images=1, keywords=["垃圾", "垃圾桶"])
