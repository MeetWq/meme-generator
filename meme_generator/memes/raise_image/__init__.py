from io import BytesIO
from pathlib import Path
from typing import List

from meme_generator import add_meme
from pil_utils import BuildImage

img_dir = Path(__file__).parent / "images"


def raise_image(images: List[BuildImage], texts, args) -> BytesIO:
    inner_img = images[0]
    img = BuildImage.open(img_dir / "raise_image.png")
    img = img.paste(
        inner_img.resize((599, 386), keep_ratio=True),
        (134, 91),
        alpha=True,
        below=True,
    )
    return img.save_png()


add_meme(
    "raise_image",
    raise_image,
    min_images=1,
    max_images=1,
    keywords=["举"],
)
