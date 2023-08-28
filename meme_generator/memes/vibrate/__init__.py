from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

img_dir = Path(__file__).parent / "images"


def vibrate(images: List[BuildImage], texts, args):
    def maker(i: int) -> Maker:
        def make(img: BuildImage) -> BuildImage:
            img = img.convert("RGBA").square()
            w = img.size[0]
            locs = [
                (0, 0),
                (w // 25, w // 25),
                (w // 50, w // 50),
                (0, w // 25),
                (w // 25, 0),
            ]
            frame = BuildImage.new("RGBA", (w + w // 25, w + w // 25), "white")
            frame.paste(img, locs[i], alpha=True)
            return frame

        return make

    return make_gif_or_combined_gif(
        images[0], maker, 5, 0.05, FrameAlignPolicy.extend_loop
    )


add_meme("vibrate", vibrate, min_images=1, max_images=1, keywords=["震动"])
