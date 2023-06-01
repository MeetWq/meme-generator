from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import MemeArgsModel, add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def OSHI_NO_KO(images: List[BuildImage], texts, args: MemeArgsModel):
    img = images[0]
    img = img.convert("RGBA").resize_width(691)
    if texts:
        text = texts[0]
    elif args.user_infos:
        text = args.user_infos[0].name
    else:
        text = "网友"

    if len(text) > 2:
        text = text[0:2]
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img, (0, 0), alpha=True, below=True)
    frame.draw_text(
        (433, 28, 589, 184),
        text,
        fontsize=76,
        max_fontsize=80,
        min_fontsize=60,
        stroke_ratio=0.1,
        stroke_fill="white",
    )
    return frame.save_jpg()


add_meme(
    "oshi_no_zo",
    OSHI_NO_KO,
    min_images=1,
    max_images=1,
    max_texts=1,
    default_texts=["网友"],
    keywords=["我推的网友"],
)
