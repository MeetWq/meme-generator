from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

img_dir = Path(__file__).parent / "images"


def capoo_strike(images: List[BuildImage], texts, args):
    params = (
        (((0, 4), (153, 0), (138, 105), (0, 157)), (28, 47)),
        (((1, 13), (151, 0), (130, 104), (0, 156)), (28, 48)),
        (((9, 10), (156, 0), (152, 108), (0, 155)), (18, 51)),
        (((0, 21), (150, 0), (146, 115), (7, 145)), (17, 53)),
        (((0, 19), (156, 0), (199, 109), (31, 145)), (2, 62)),
        (((0, 28), (156, 0), (171, 115), (12, 154)), (16, 58)),
        (((0, 25), (157, 0), (169, 113), (13, 147)), (18, 63)),
    )

    def maker(i: int) -> Maker:
        def make(img: BuildImage) -> BuildImage:
            img = img.convert("RGBA").resize((200, 160), keep_ratio=True)
            points, pos = params[i]
            frame = BuildImage.open(img_dir / f"{i}.png")
            frame.paste(img.perspective(points), pos, below=True)
            return frame

        return make

    return make_gif_or_combined_gif(
        images[0], maker, 7, 0.05, FrameAlignPolicy.extend_loop
    )


add_meme(
    "capoo_strike",
    capoo_strike,
    min_images=1,
    max_images=1,
    keywords=["咖波撞", "咖波头槌"],
)
