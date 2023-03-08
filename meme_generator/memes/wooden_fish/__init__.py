from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def wooden_fish(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").resize((85, 85))
    frames = [
        BuildImage.open(img_dir / f"{i}.png").paste(img, (116, 153), below=True).image
        for i in range(66)
    ]
    return save_gif(frames, 0.1)


add_meme("wooden_fish", wooden_fish, min_images=1, max_images=1, keywords=["木鱼"])
