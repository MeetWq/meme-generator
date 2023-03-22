from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

img_dir = Path(__file__).parent / "images"


def hit_screen(images: List[BuildImage], texts, args):
    params = (
        (((1, 10), (138, 1), (140, 119), (7, 154)), (32, 37)),
        (((1, 10), (138, 1), (140, 121), (7, 154)), (32, 37)),
        (((1, 10), (138, 1), (139, 125), (10, 159)), (32, 37)),
        (((1, 12), (136, 1), (137, 125), (8, 159)), (34, 37)),
        (((1, 9), (137, 1), (139, 122), (9, 154)), (35, 41)),
        (((1, 8), (144, 1), (144, 123), (12, 155)), (30, 45)),
        (((1, 8), (140, 1), (141, 121), (10, 155)), (29, 49)),
        (((1, 9), (140, 1), (139, 118), (10, 153)), (27, 53)),
        (((1, 7), (144, 1), (145, 117), (13, 153)), (19, 57)),
        (((1, 7), (144, 1), (143, 116), (13, 153)), (19, 57)),
        (((1, 8), (139, 1), (141, 119), (12, 154)), (19, 55)),
        (((1, 13), (140, 1), (143, 117), (12, 156)), (16, 57)),
        (((1, 10), (138, 1), (142, 117), (11, 149)), (14, 61)),
        (((1, 10), (141, 1), (148, 125), (13, 153)), (11, 57)),
        (((1, 12), (141, 1), (147, 130), (16, 150)), (11, 60)),
        (((1, 15), (165, 1), (175, 135), (1, 171)), (-6, 46)),
    )

    def maker(i: int) -> Maker:
        def make(img: BuildImage) -> BuildImage:
            img = img.convert("RGBA").resize((140, 120), keep_ratio=True)
            frame = BuildImage.open(img_dir / f"{i}.png")
            if 6 <= i < 22:
                points, pos = params[i - 6]
                frame.paste(img.perspective(points), pos, below=True)
            return frame

        return make

    return make_gif_or_combined_gif(
        images[0], maker, 29, 0.2, FrameAlignPolicy.extend_first
    )


add_meme("hit_screen", hit_screen, min_images=1, max_images=1, keywords=["打穿", "打穿屏幕"])
