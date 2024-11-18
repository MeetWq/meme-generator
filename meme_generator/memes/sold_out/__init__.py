from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def sold_out(images: list[BuildImage], texts, args):
    icon = BuildImage.open(img_dir / "0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        frame = imgs[0].convert("RGBA")
        if frame.width > frame.height:
            frame = frame.resize_height(600)
        else:
            frame = frame.resize_width(600)
        mask = BuildImage.new("RGBA", frame.size, (0, 0, 0, 64))
        frame.paste(mask, alpha=True)
        return frame.paste(
            icon,
            ((frame.width - icon.height) // 2, (frame.height - icon.height) // 2),
            alpha=True,
        )

    return make_jpg_or_gif(images, make)


add_meme(
    "sold_out",
    sold_out,
    min_images=1,
    max_images=1,
    keywords=["卖掉了"],
    date_created=datetime(2024, 11, 18),
    date_modified=datetime(2024, 11, 18),
)
