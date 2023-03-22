from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

img_dir = Path(__file__).parent / "images"


def confuse(images: List[BuildImage], texts, args):
    img_w = min(images[0].width, 500)

    def maker(i: int) -> Maker:
        def make(img: BuildImage) -> BuildImage:
            img = img.convert("RGBA").resize_width(img_w)
            frame = BuildImage.open(img_dir / f"{i}.png").resize(
                img.size, keep_ratio=True
            )
            bg = BuildImage.new("RGB", img.size, "white")
            bg.paste(img, alpha=True).paste(frame, alpha=True)
            return bg

        return make

    return make_gif_or_combined_gif(
        images[0], maker, 100, 0.02, FrameAlignPolicy.extend_loop, input_based=True
    )


add_meme("confuse", confuse, min_images=1, max_images=1, keywords=["迷惑"])
