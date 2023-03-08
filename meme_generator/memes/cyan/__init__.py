from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme


def cyan(images: List[BuildImage], texts, args):
    color = (78, 114, 184)
    frame = images[0].convert("RGB").square().resize((500, 500)).color_mask(color)
    frame.draw_text(
        (400, 40, 480, 280),
        "群\n青",
        max_fontsize=80,
        weight="bold",
        fill="white",
        stroke_ratio=0.04,
        stroke_fill=color,
    ).draw_text(
        (200, 270, 480, 350),
        "YOASOBI",
        halign="right",
        max_fontsize=40,
        fill="white",
        stroke_ratio=0.06,
        stroke_fill=color,
    )
    return frame.save_jpg()


add_meme("cyan", cyan, min_images=1, max_images=1, keywords=["群青"])
