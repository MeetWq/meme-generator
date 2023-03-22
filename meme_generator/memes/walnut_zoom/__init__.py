from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

img_dir = Path(__file__).parent / "images"


def walnut_zoom(images: List[BuildImage], texts, args):
    # fmt: off
    locs = (
        (-222, 30, 695, 430), (-212, 30, 695, 430), (0, 30, 695, 430), (41, 26, 695, 430),
        (-100, -67, 922, 570), (-172, -113, 1059, 655), (-273, -192, 1217, 753)
    )
    seq = [0, 0, 0, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 6, 6, 6, 6]
    # fmt: on

    def maker(i: int) -> Maker:
        def make(img: BuildImage) -> BuildImage:
            frame = BuildImage.open(img_dir / f"{i}.png")
            x, y, w, h = locs[seq[i]]
            img = img.convert("RGBA").resize((w, h), keep_ratio=True)
            frame.paste(img.rotate(4.2, expand=True), (x, y), below=True)
            return frame

        return make

    return make_gif_or_combined_gif(
        images[0], maker, 24, 0.2, FrameAlignPolicy.extend_last
    )


add_meme("walnut_zoom", walnut_zoom, min_images=1, max_images=1, keywords=["胡桃放大"])
