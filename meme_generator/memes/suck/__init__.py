from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def suck(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").square()
    # fmt: off
    locs = [(82, 100, 130, 119), (82, 94, 126, 125), (82, 120, 128, 99), (81, 164, 132, 55),
            (79, 163, 132, 55), (82, 140, 127, 79), (83, 152, 125, 67), (75, 157, 140, 62),
            (72, 165, 144, 54), (80, 132, 128, 87), (81, 127, 127, 92), (79, 111, 132, 108)]
    # fmt: on
    frames: List[IMG] = []
    for i in range(12):
        bg = BuildImage.open(img_dir / f"{i}.png")
        frame = BuildImage.new("RGBA", bg.size, "white")
        x, y, w, h = locs[i]
        frame.paste(img.resize((w, h)), (x, y), alpha=True).paste(bg, alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.08)


add_meme("suck", suck, min_images=1, max_images=1, keywords=["吸", "嗦"])
