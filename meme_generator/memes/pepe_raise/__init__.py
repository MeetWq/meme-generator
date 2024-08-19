from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

img_dir = Path(__file__).parent / "images"


def pepe_raise(images: list[BuildImage], texts, args):
    # fmt: off
    left_locs = [
        (107, 30), (107, 30), (95, 45),
        (80, 160), (80, 160), (70, 98),
    ]
    right_locs = [
        (320, 145), (320, 145), (330, 130),
        (300, 50), (300, 50), (323, 80),
    ]
    # fmt: on
    frame_num = 6

    def maker(i: int) -> Maker:
        def make(imgs: list[BuildImage]) -> BuildImage:
            frame = BuildImage.open(img_dir / f"{i}.png")
            left_img = imgs[0].convert("RGBA").circle().resize((100, 100))
            right_img = imgs[1].convert("RGBA").circle().resize((100, 100))
            frame.paste(left_img, left_locs[i], alpha=True)
            frame.paste(right_img, right_locs[i], alpha=True)
            return frame

        return make

    return make_gif_or_combined_gif(
        images, maker, frame_num, 0.06, FrameAlignPolicy.extend_loop
    )


add_meme(
    "pepe_raise",
    pepe_raise,
    min_images=2,
    max_images=2,
    keywords=["佩佩举"],
    tags=MemeTags.arknights,
    date_created=datetime(2024, 8, 18),
    date_modified=datetime(2024, 8, 18),
)
