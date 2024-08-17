from datetime import datetime
from io import BytesIO
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def raise_image(images: list[BuildImage], texts, args) -> BytesIO:
    inner_size = (599, 386)
    paste_pos = (134, 91)

    bg = BuildImage.open(img_dir / "raise_image.png")

    def make_frame(imgs: list[BuildImage]) -> BuildImage:
        inner_frame = BuildImage.new("RGBA", inner_size, "white")
        inner_frame = inner_frame.paste(
            imgs[0].convert("RGBA").resize(inner_size, keep_ratio=True),
            alpha=True,
        )
        return bg.copy().paste(inner_frame, paste_pos, alpha=True, below=True)

    return make_jpg_or_gif(images, make_frame)


add_meme(
    "raise_image",
    raise_image,
    min_images=1,
    max_images=1,
    keywords=["举"],
    date_created=datetime(2023, 8, 9),
    date_modified=datetime(2023, 8, 9),
)
