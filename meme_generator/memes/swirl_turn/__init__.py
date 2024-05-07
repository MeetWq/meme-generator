import math
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif


def swirl_turn(images: List[BuildImage], texts, args):
    frame_num = 40

    def maker(i: int) -> Maker:
        def make(img: BuildImage) -> BuildImage:
            img = img.convert("RGBA").circle().resize((100, 100))
            start_angle = i * 360 / frame_num
            frame = BuildImage.new("RGBA", (300, 300))
            num = 24
            for j in range(num):
                angle = start_angle + j * 360 / num
                x = 150 + 75 * math.cos(math.radians(angle))
                y = 150 + 75 * math.sin(math.radians(angle))
                frame.paste(img, (round(x - 50), round(y - 50)), alpha=True)
            return frame

        return make

    return make_gif_or_combined_gif(
        images[0], maker, frame_num, 0.02, FrameAlignPolicy.extend_loop
    )


add_meme(
    "swirl_turn",
    swirl_turn,
    min_images=1,
    max_images=1,
    keywords=["回旋转", "漩涡转"],
)
