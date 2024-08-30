from datetime import datetime
from pathlib import Path

from meme_generator import add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif
from pil_utils import BuildImage

img_dir = Path(__file__).parent / "images"


def jerk_off(images: list[BuildImage], texts, args):
    jerk_w, jerk_h = BuildImage.open(img_dir / "0.png").size
    img_w, img_h = images[0].size
    if img_w / img_h > jerk_w / jerk_h:
        frame_h = jerk_h
        frame_w = round(frame_h * img_w / img_h)
    else:
        frame_w = jerk_w
        frame_h = round(frame_w * img_h / img_w)

    def maker(i: int) -> Maker:
        def make(imgs: list[BuildImage]) -> BuildImage:
            frame = imgs[0].convert("RGBA").resize((frame_w, frame_h), keep_ratio=True)
            jerk = BuildImage.open(img_dir / f"{i}.png")
            frame.paste(jerk, ((frame_w - jerk_w) // 2, frame_h - jerk_h), alpha=True)
            return frame

        return make

    return make_gif_or_combined_gif(images, maker, 8, 0.1, FrameAlignPolicy.extend_loop)


add_meme(
    "jerk_off",
    jerk_off,
    min_images=1,
    max_images=1,
    keywords=["打胶"],
    date_created=datetime(2024, 8, 4),
    date_modified=datetime(2024, 8, 4),
)
