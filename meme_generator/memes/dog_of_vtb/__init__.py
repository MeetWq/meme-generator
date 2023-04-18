from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def dog_of_vtb(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").resize((150, 100), inside=True, bg_color="white")
    params = [(97, 32), ((0, 0), (579, 0), (584, 430), (5, 440))]

    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img.perspective(params[1]), params[0], below=True)

    return frame.save_jpg()


add_meme(
    "dog_of_vtb",
    dog_of_vtb,
    min_images=1,
    max_images=1,
    keywords=["管人痴"],
)
