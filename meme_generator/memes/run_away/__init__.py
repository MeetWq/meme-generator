from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

img_dir = Path(__file__).parent / "images"


def run_away(images: list[BuildImage], texts, args):
    miku_w, miku_h = BuildImage.open(img_dir / "0.png").size
    img_w, img_h = images[0].size
    ratio = 1.2
    if img_w > img_h:
        frame_h = round(miku_h * ratio)
        frame_w = round(frame_h * img_w / img_h)
    else:
        frame_w = round(miku_w * ratio)
        frame_h = round(frame_w * img_h / img_w)

    def maker(i: int) -> Maker:
        def make(imgs: list[BuildImage]) -> BuildImage:
            frame = imgs[0].convert("RGBA").resize((frame_w, frame_h), keep_ratio=True)
            miku = BuildImage.open(img_dir / f"{i}.png")
            frame.paste(miku, (frame_w - miku_w, frame_h - miku_h), alpha=True)
            return frame

        return make

    return make_gif_or_combined_gif(
        images, maker, 42, 0.03, FrameAlignPolicy.extend_loop
    )


add_meme(
    "run_away",
    run_away,
    min_images=1,
    max_images=1,
    keywords=["快逃"],
    tags=MemeTags.miku,
    date_created=datetime(2024, 7, 23),
    date_modified=datetime(2024, 7, 23),
)
