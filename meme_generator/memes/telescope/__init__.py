from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

img_dir = Path(__file__).parent / "images"


def telescope(images: list[BuildImage], texts, args):
    def maker(i: int) -> Maker:
        def make(imgs: list[BuildImage]) -> BuildImage:
            img = imgs[0].convert("RGBA").square()
            img_big = img.resize((600, 600))
            img_small = img.resize((230, 230))
            frame = BuildImage.open(img_dir / f"{i}.png")
            if 4 <= i < 18:
                x = -167 + (i - 4) * 4
                y = -361 + (i - 4) * 7
                frame.paste(img_big, (x, y), below=True)
            elif 23 <= i < 38:
                x = -90 + (i - 23) * 5
                y = -245 + (i - 23) * 5
                frame.paste(img_big, (x, y), below=True)
            elif 43 <= i < 46:
                x = -15
                y = -210
                frame.paste(img_big, (x, y), below=True)
            elif 46 <= i < 57:
                x = 8
                y = -21
                frame.paste(img_small, (x, y), below=True)
            return frame

        return make

    return make_gif_or_combined_gif(
        images, maker, 69, 0.1, FrameAlignPolicy.extend_first
    )


add_meme(
    "telescope",
    telescope,
    min_images=1,
    max_images=1,
    keywords=["望远镜"],
    date_created=datetime(2024, 1, 18),
    date_modified=datetime(2024, 1, 18),
)
