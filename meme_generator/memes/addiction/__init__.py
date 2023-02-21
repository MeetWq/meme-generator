from typing import List
from pathlib import Path
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def addiction(images: List[BuildImage], texts: List[str], args):
    img = images[0]
    frame = BuildImage.open(img_dir / "0.png")

    if texts:
        text = texts[0]
        frame = frame.resize_canvas((246, 286), direction="north", bg_color="white")
        try:
            frame.draw_text((10, 246, 236, 286), texts[0], max_fontsize=45)
        except ValueError:
            raise TextOverLength(text)

    def make(img: BuildImage) -> BuildImage:
        return frame.copy().paste(img.resize((91, 91), keep_ratio=True), (0, 0))

    return make_jpg_or_gif(img, make)


add_meme(
    "addiction",
    addiction,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    keywords=["上瘾", "毒瘾发作"],
)
