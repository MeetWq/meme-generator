from datetime import datetime
from pathlib import Path

from meme_generator import add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif
from pil_utils import BuildImage

img_dir = Path(__file__).parent / "images"


def shoot(images: list[BuildImage], texts, args):
    def maker(i: int) -> Maker:
        def make(imgs: list[BuildImage]) -> BuildImage:
            img = imgs[0].convert("RGBA").resize((160, 97), keep_ratio=True)
            fluid = BuildImage.open(img_dir / f"{i}.png")
            img.paste(fluid, alpha=True)
            return img

        return make

    return make_gif_or_combined_gif(
        images, maker, 13, 0.15, FrameAlignPolicy.extend_loop
    )


add_meme(
    "shoot",
    shoot,
    min_images=1,
    max_images=1,
    keywords=["射", "🐍"],
    date_created=datetime(2024, 8, 19),
    date_modified=datetime(2024, 8, 19),
)
