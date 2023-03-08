from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def printing(images: List[BuildImage], texts, args):
    img = (
        images[0]
        .convert("RGBA")
        .resize(
            (304, 174),
            keep_ratio=True,
            inside=True,
            bg_color="white",
            direction="south",
        )
    )
    frames = [BuildImage.open(img_dir / f"{i}.png") for i in range(115)]
    for i in range(50, 115):
        frames[i].paste(img, (146, 164), below=True)
    frames = [frame.image for frame in frames]
    return save_gif(frames, 0.05)


add_meme("printing", printing, min_images=1, max_images=1, keywords=["打印"])
