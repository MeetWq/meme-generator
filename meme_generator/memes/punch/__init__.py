from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def punch(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").square().resize((260, 260))
    frames: List[IMG] = []
    # fmt: off
    locs = [
        (-50, 20), (-40, 10), (-30, 0), (-20, -10), (-10, -10), (0, 0),
        (10, 10), (20, 20), (10, 10), (0, 0), (-10, -10), (10, 0), (-30, 10)
    ]
    # fmt: on
    for i in range(13):
        fist = BuildImage.open(img_dir / f"{i}.png")
        frame = BuildImage.new("RGBA", fist.size, "white")
        x, y = locs[i]
        frame.paste(img, (x, y - 15), alpha=True).paste(fist, alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.03)


add_meme("punch", punch, min_images=1, max_images=1, keywords=["打拳"])
