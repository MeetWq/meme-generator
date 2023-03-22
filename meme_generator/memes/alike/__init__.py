from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif


def alike(images: List[BuildImage], texts, args):
    frame = BuildImage.new("RGBA", (470, 180), "white")
    frame.draw_text(
        (10, 10, 185, 140), "你怎么跟", max_fontsize=40, min_fontsize=30, halign="right"
    ).draw_text(
        (365, 10, 460, 140), "一样", max_fontsize=40, min_fontsize=30, halign="left"
    )

    def make(img: BuildImage) -> BuildImage:
        img = img.convert("RGBA").resize((150, 150), keep_ratio=True)
        return frame.copy().paste(img, (200, 15), alpha=True)

    return make_jpg_or_gif(images[0], make)


add_meme("alike", alike, min_images=1, max_images=1, keywords=["一样"])
