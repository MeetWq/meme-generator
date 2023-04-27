import random
from pathlib import Path
from typing import List, Tuple

from PIL.Image import Image as IMG
from PIL.Image import Palette
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def get_dominant_colors(img: IMG) -> List[Tuple[int, int, int]]:
    img = img.convert("P", palette=Palette.ADAPTIVE, colors=20)
    palette = img.getpalette()
    assert palette
    color_indexs = sorted(img.getcolors(), reverse=True)
    colors = [tuple(palette[i * 3 : i * 3 + 3]) for _, i in color_indexs]
    colors = list(
        filter(lambda c: c[0] * 0.299 + c[1] * 0.578 + c[2] * 0.114 < 200, colors)
    )
    return colors


def dont_touch(images: List[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")
    mask = BuildImage.open(img_dir / "mask.png").convert("L")

    def paste_random_blocks(img: BuildImage, colors: List[Tuple[int, int, int]]):
        x1, y1, x2, y2 = 200, 300, 400, 650
        block_locs = []
        for _ in range(150):
            x = random.randint(x1, x2)
            y = random.randint(y1, y2)
            if mask.image.getpixel((x, y)) == 0:
                continue
            if any(abs(x - x_) < 13 and abs(y - y_) < 13 for x_, y_ in block_locs):
                continue
            block_locs.append((x, y))
            color = random.choice(colors)
            block = BuildImage.new("RGBA", (10, 10), color)
            block = block.rotate(45, expand=True)
            img.paste(block, (x, y), alpha=True)

    def make(img: BuildImage) -> BuildImage:
        img_frame = frame.copy()
        colors = get_dominant_colors(img.image)
        paste_random_blocks(img_frame, colors)
        img = img.convert("RGBA").resize((250, 250), keep_ratio=True, inside=True)
        return img_frame.paste(img, (25, 460), alpha=True)

    return make_jpg_or_gif(images[0], make)


add_meme("dont_touch", dont_touch, min_images=1, max_images=1, keywords=["别碰"])
