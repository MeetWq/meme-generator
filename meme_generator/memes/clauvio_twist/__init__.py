from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

img_dir = Path(__file__).parent / "images"


def clauvio_twist(images: list[BuildImage], texts, args):
    params = [
        (0, (45, 144)),  # 0
        (0, (45, 144)),  # 1
        (0, (45, 144)),  # 2
        (2, (45, 141)),  # 3
        (4, (45, 141)),  # 4
        (8, (40, 141)),  # 5
        (12, (38, 142)),  # 6
        (30, (32, 148)),  # 7
        (75, (25, 158)),  # 8
        (115, (0, 160)),  # 9
        (130, (0, 160)),  # 10
        (125, (0, 155)),  # 11
        (120, (0, 150)),  # 12
        (115, (0, 148)),  # 13
        (110, (5, 146)),  # 14
        (85, (14, 146)),  # 15
        (70, (19, 146)),  # 16
        (45, (28, 144)),  # 17
        (37, (38, 141)),  # 18
        (10, (42, 144)),  # 19
    ]

    def maker(i: int) -> Maker:
        def make(imgs: list[BuildImage]) -> BuildImage:
            img = imgs[0].convert("RGBA").resize((100, 100), keep_ratio=True).circle()
            angle, pos = params[i % 20]
            bg = BuildImage.open(img_dir / f"{i}.png")
            return bg.paste(img.rotate(angle), pos, alpha=True)

        return make

    return make_gif_or_combined_gif(
        images, maker, 40, 0.05, FrameAlignPolicy.extend_loop
    )


add_meme(
    "clauvio_twist",
    clauvio_twist,
    min_images=1,
    max_images=1,
    keywords=["鼠鼠搓"],
    date_created=datetime(2024, 8, 31),
    date_modified=datetime(2024, 8, 31),
)
