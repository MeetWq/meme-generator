from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_png_or_gif

img_dir = Path(__file__).parent / "images"


def mihoyo(images: List[BuildImage], texts, args):
    mask = BuildImage.new("RGBA", (500, 60), (53, 49, 65, 230))
    logo = BuildImage.open(img_dir / "logo.png").resize_height(50)

    def make(img: BuildImage) -> BuildImage:
        img = img.convert("RGBA").resize((500, 500), keep_ratio=True)
        img.paste(mask, (0, 440), alpha=True)
        img.paste(logo, ((img.width - logo.width) // 2, 445), alpha=True)
        return img.circle_corner(100)

    return make_png_or_gif(images[0], make)


add_meme("mihoyo", mihoyo, min_images=1, max_images=1, keywords=["米哈游"])
