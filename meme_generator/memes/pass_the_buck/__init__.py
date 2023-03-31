from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def pass_the_buck(images: List[BuildImage], texts: List[str], args):
    img = images[0].convert("RGBA").square().resize((27, 27))
    frames: List[IMG] = []
    locs = [(2, 26), (10, 24), (15, 27), (17, 29), (10, 20), (2, 29), (3, 31), (1, 30)]
    for i in range(8):
        frame = BuildImage.open(img_dir / f"{i}.png")
        if texts:
            text = texts[0]
            try:
                frame.draw_text(
                    (0, 0, frame.width, 20), text, max_fontsize=20, min_fontsize=10
                )
            except ValueError:
                raise TextOverLength(text)
        frame.paste(img, locs[i], alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.1)


add_meme(
    "pass_the_buck",
    pass_the_buck,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=["你写!"],
    keywords=["推锅", "甩锅"],
)
