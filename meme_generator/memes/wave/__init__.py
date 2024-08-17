import math
from datetime import datetime

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif


def wave(images: list[BuildImage], texts, args):
    img_w = min(max(images[0].width, 360), 720)
    period = img_w / 6
    amp = img_w / 60
    frame_num = 8

    def maker(i: int) -> Maker:
        def sin(x):
            return (
                amp * math.sin(2 * math.pi / period * (x + i * period / frame_num)) / 2
            )

        def make(imgs: list[BuildImage]) -> BuildImage:
            img = imgs[0].convert("RGBA").resize_width(img_w)
            img_h = img.height
            frame = img.copy()
            for i in range(img_w):
                for j in range(img_h):
                    dx = int(sin(i) * (img_h - j) / img_h)
                    dy = int(sin(j) * j / img_h)
                    if 0 <= i + dx < img_w and 0 <= j + dy < img_h:
                        frame.image.putpixel(
                            (i, j),
                            img.image.getpixel((i + dx, j + dy)),  # type: ignore
                        )

            frame = frame.resize_canvas((int(img_w - amp), int(img_h - amp)))
            return frame

        return make

    return make_gif_or_combined_gif(
        images, maker, frame_num, 0.01, FrameAlignPolicy.extend_loop
    )


add_meme(
    "wave",
    wave,
    min_images=1,
    max_images=1,
    keywords=["波纹"],
    date_created=datetime(2022, 10, 26),
    date_modified=datetime(2023, 2, 14),
)
