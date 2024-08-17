from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def let_me_in(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize((510, 810), keep_ratio=True)
        return frame.copy().paste(img, (320, 0), below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "let_me_in",
    let_me_in,
    min_images=1,
    max_images=1,
    keywords=["让我进去"],
    date_created=datetime(2024, 7, 18),
    date_modified=datetime(2024, 7, 18),
)
