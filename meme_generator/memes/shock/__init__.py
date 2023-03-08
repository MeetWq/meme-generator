import random
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif


def shock(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").square().resize((300, 300))
    frames: List[IMG] = []
    for i in range(30):
        frames.append(
            img.motion_blur(random.randint(-90, 90), random.randint(0, 50))
            .rotate(random.randint(-20, 20))
            .image
        )
    return save_gif(frames, 0.01)


add_meme("shock", shock, min_images=1, max_images=1, keywords=["震惊"])
