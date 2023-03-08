from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def eat(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").square().resize((34, 34))
    frames = []
    for i in range(3):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(img, (2, 38), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.05)


add_meme("eat", eat, min_images=1, max_images=1, keywords=["吃"])
