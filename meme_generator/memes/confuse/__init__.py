from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

img_dir = Path(__file__).parent / "images"


def confuse(images: list[BuildImage], texts, args):
    img_w = min(images[0].width, 500)

    def maker(i: int) -> Maker:
        def make(imgs: list[BuildImage]) -> BuildImage:
            img = imgs[0].convert("RGBA").resize_width(img_w)
            frame = BuildImage.open(img_dir / f"{i}.png").resize(
                img.size, keep_ratio=True
            )
            bg = BuildImage.new("RGB", img.size, "white")
            bg.paste(img, alpha=True).paste(frame, alpha=True)
            return bg

        return make

    return make_gif_or_combined_gif(
        images, maker, 100, 0.02, FrameAlignPolicy.extend_loop
    )


add_meme(
    "confuse",
    confuse,
    min_images=1,
    max_images=1,
    keywords=["迷惑"],
    date_created=datetime(2022, 9, 4),
    date_modified=datetime(2023, 2, 14),
)
