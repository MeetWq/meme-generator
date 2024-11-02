import math
import random
from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

img_dir = Path(__file__).parent / "images"


def shake_head(images: list[BuildImage], texts, args):
    img_w, img_h = images[0].size
    padding_w = img_w // 10
    padding_h = img_h // 10
    dw = max(padding_w // 8, 1)
    dh = max(padding_h // 8, 1)
    frame_w = img_w - padding_w * 2
    frame_h = img_h - padding_h * 2
    frame_num = 20
    dt = 2 * math.pi / frame_num
    frame = BuildImage.new("RGBA", (frame_w, frame_h))

    def maker(i: int) -> Maker:
        def make(imgs: list[BuildImage]) -> BuildImage:
            img = imgs[0].convert("RGBA")
            x = round(
                padding_w * math.sin(-i * dt)
                - padding_w
                + (2 * random.random() - 1) * dw
            )
            y = round(
                padding_h * math.cos(-i * dt)
                - padding_h
                + (2 * random.random() - 1) * dh
            )
            return frame.copy().paste(img, (x, y), alpha=True)

        return make

    return make_gif_or_combined_gif(
        images, maker, frame_num, 0.02, FrameAlignPolicy.extend_loop
    )


add_meme(
    "shake_head",
    shake_head,
    min_images=1,
    max_images=1,
    keywords=["晃脑"],
    date_created=datetime(2024, 10, 31),
    date_modified=datetime(2024, 10, 31),
)
