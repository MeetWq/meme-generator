import math
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif


def wave(images: List[BuildImage], texts, args):
    img = images[0]
    img_w = min(max(img.width, 360), 720)
    period = img_w / 6
    amp = img_w / 60
    frame_num = 8
    phase = 0
    sin = lambda x: amp * math.sin(2 * math.pi / period * (x + phase)) / 2

    def maker(i: int) -> Maker:
        def make(img: BuildImage) -> BuildImage:
            img = img.convert("RGBA").resize_width(img_w)
            img_h = img.height
            frame = img.copy()
            for i in range(img_w):
                for j in range(img_h):
                    dx = int(sin(i) * (img_h - j) / img_h)
                    dy = int(sin(j) * j / img_h)
                    if 0 <= i + dx < img_w and 0 <= j + dy < img_h:
                        frame.image.putpixel(
                            (i, j), img.image.getpixel((i + dx, j + dy))
                        )

            frame = frame.resize_canvas((int(img_w - amp), int(img_h - amp)))
            nonlocal phase
            phase += period / frame_num
            return frame

        return make

    return make_gif_or_combined_gif(
        img, maker, frame_num, 0.01, FrameAlignPolicy.extend_loop
    )


add_meme("wave", wave, min_images=1, max_images=1, keywords=["波纹"])
