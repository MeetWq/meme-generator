import math
from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags

img_dir = Path(__file__).parent / "images"


def lost_dog(images: list[BuildImage], texts, args):
    k = 2
    w_ = 663 * k
    w = 540 * k
    h = 540 * k
    r = 466 * k
    img = images[0].convert("RGBA").resize((w_, h), keep_ratio=True)
    img_new = BuildImage.new("RGBA", (w, h))
    for x in range(w):
        for y in range(h):
            theta = math.asin(abs(x - w / 2) / r)
            x_ = round(w_ / 2 + (x - w / 2) / math.cos(theta))
            y_ = round(h / 2 + (y - h / 2) / math.cos(theta))
            if 0 <= x_ < w_ and 0 <= y_ < h:
                img_new.image.putpixel((x, y), img.image.getpixel((x_, y_)))  # type: ignore
    img_new = img_new.resize((w // k, h // k))
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img_new, (295, 165), below=True)
    return frame.save_jpg()


add_meme(
    "lost_dog",
    lost_dog,
    min_images=1,
    max_images=1,
    keywords=["寻狗启事"],
    tags=MemeTags.ayaka,
    date_created=datetime(2024, 1, 19),
    date_modified=datetime(2024, 1, 20),
)
