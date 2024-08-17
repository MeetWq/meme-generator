from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def out(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "out.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA")
        out = frame.copy().resize_width(int(img.width * 0.5), keep_ratio=True)
        return img.paste(
            out,
            (
                min(img.width - out.width - 10, int(img.width * 0.4)),
                min(img.height - out.height - 10, int(img.height * 0.7)),
            ),
            alpha=True,
        )

    return make_jpg_or_gif(images, make)


add_meme(
    "out",
    out,
    min_images=1,
    max_images=1,
    keywords=["out"],
    date_created=datetime(2024, 4, 26),
    date_modified=datetime(2024, 4, 26),
)
