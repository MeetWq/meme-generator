from io import BytesIO
from pathlib import Path
from typing import List

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif
from pil_utils import BuildImage

img_dir = Path(__file__).parent / "images"


def raise_image(images: List[BuildImage], texts, args) -> BytesIO:  # noqa: ARG001
    inner_size = (599, 386)
    paste_pos = (134, 91)

    bg = BuildImage.open(img_dir / "raise_image.png")

    def make_frame(img: BuildImage) -> BuildImage:
        img = img.resize(inner_size, keep_ratio=True)
        inner_frame = BuildImage.new("RGBA", inner_size, "white").paste(img, alpha=True)
        return bg.copy().paste(inner_frame, paste_pos, alpha=True, below=True)

    return make_jpg_or_gif(images[0], make_frame)


add_meme(
    "raise_image",
    raise_image,
    min_images=1,
    max_images=1,
    keywords=["举"],
)
