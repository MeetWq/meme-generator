from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import MemeArgsModel, add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def coupon(images: List[BuildImage], texts: List[str], args: MemeArgsModel):
    img = images[0].convert("RGBA").circle().resize((60, 60))
    name = args.user_infos[0].name if args.user_infos else ""
    text = (texts[0] if texts else f"{name}陪睡券") + "\n（永久有效）"

    text_img = BuildImage.new("RGBA", (250, 100))
    try:
        text_img.draw_text(
            (0, 0, text_img.width, text_img.height),
            text,
            lines_align="center",
            max_fontsize=30,
            min_fontsize=15,
        )
    except ValueError:
        raise TextOverLength(text)

    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img.rotate(22, expand=True), (164, 85), alpha=True)
    frame.paste(text_img.rotate(22, expand=True), (94, 108), alpha=True)
    return frame.save_jpg()


add_meme(
    "coupon",
    coupon,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    keywords=["兑换券"],
)
