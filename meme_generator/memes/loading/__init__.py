from pathlib import Path
from typing import List

from PIL import ImageFilter
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def loading(images: List[BuildImage], texts, args):
    img_big = images[0].convert("RGBA").resize_width(500)
    img_big = img_big.filter(ImageFilter.GaussianBlur(radius=3))
    h1 = img_big.height
    mask = BuildImage.new("RGBA", img_big.size, (0, 0, 0, 32))
    icon = BuildImage.open(img_dir / "icon.png")
    img_big.paste(mask, alpha=True).paste(icon, (200, int(h1 / 2) - 50), alpha=True)

    def make(img: BuildImage) -> BuildImage:
        img_small = img.convert("RGBA").resize_width(100)
        h2 = max(img_small.height, 80)
        frame = BuildImage.new("RGBA", (500, h1 + h2 + 10), "white")
        frame.paste(img_big, alpha=True).paste(
            img_small, (100, h1 + 5 + (h2 - img_small.height) // 2), alpha=True
        )
        frame.draw_text(
            (210, h1 + 5, 480, h1 + h2 + 5), "不出来", halign="left", max_fontsize=60
        )
        return frame

    return make_jpg_or_gif(images[0], make)


add_meme("loading", loading, min_images=1, max_images=1, keywords=["加载中"])
