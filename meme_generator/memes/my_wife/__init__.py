from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def my_wife(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").resize_width(400)
    img_w, img_h = img.size
    frame = BuildImage.new("RGBA", (650, img_h + 500), "white")
    frame.paste(img, (int(325 - img_w / 2), 105), alpha=True)

    text = "如果你的老婆长这样"
    frame.draw_text(
        (27, 12, 27 + 596, 12 + 79),
        text,
        max_fontsize=70,
        min_fontsize=30,
        allow_wrap=True,
        lines_align="center",
        weight="bold",
    )
    text = "那么这就不是你的老婆\n这是我的老婆"
    frame.draw_text(
        (27, img_h + 120, 27 + 593, img_h + 120 + 135),
        text,
        max_fontsize=70,
        min_fontsize=30,
        allow_wrap=True,
        weight="bold",
    )
    text = "滚去找你\n自己的老婆去"
    frame.draw_text(
        (27, img_h + 295, 27 + 374, img_h + 295 + 135),
        text,
        max_fontsize=70,
        min_fontsize=30,
        allow_wrap=True,
        lines_align="center",
        weight="bold",
    )

    img_point = BuildImage.open(img_dir / "1.png").resize_width(200)
    frame.paste(img_point, (421, img_h + 270))

    return frame.save_jpg()


add_meme("my_wife", my_wife, min_images=1, max_images=1, keywords=["我老婆", "这是我老婆"])
