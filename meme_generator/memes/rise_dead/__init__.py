from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def rise_dead(images: List[BuildImage], texts, args):
    locs = [
        ((81, 55), ((0, 2), (101, 0), (103, 105), (1, 105))),
        ((74, 49), ((0, 3), (104, 0), (106, 108), (1, 108))),
        ((-66, 36), ((0, 0), (182, 5), (184, 194), (1, 185))),
        ((-231, 55), ((0, 0), (259, 4), (276, 281), (13, 278))),
    ]
    img = images[0].convert("RGBA").square().resize((150, 150))
    imgs = [img.perspective(points) for _, points in locs]
    frames: List[IMG] = []
    for i in range(34):
        frame = BuildImage.open(img_dir / f"{i}.png")
        if i <= 28:
            idx = 0 if i <= 25 else i - 25
            x, y = locs[idx][0]
            if i % 2 == 1:
                x += 1
                y -= 1
            frame.paste(imgs[idx], (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.15)


add_meme("rise_dead", rise_dead, min_images=1, max_images=1, keywords=["诈尸", "秽土转生"])
