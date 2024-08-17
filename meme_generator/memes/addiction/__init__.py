from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def addiction(images: list[BuildImage], texts: list[str], args):
    frame = BuildImage.open(img_dir / "0.png")

    if texts:
        text = texts[0]
        frame = frame.resize_canvas((246, 286), direction="north", bg_color="white")
        try:
            frame.draw_text((10, 246, 236, 286), texts[0], max_fontsize=45)
        except ValueError:
            raise TextOverLength(text)

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize((91, 91), keep_ratio=True)
        return frame.copy().paste(img, alpha=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "addiction",
    addiction,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    keywords=["上瘾", "毒瘾发作"],
    date_created=datetime(2022, 8, 17),
    date_modified=datetime(2023, 2, 14),
)
