from pathlib import Path
from typing import List

from pil_utils import BuildImage, Text2Image

from meme_generator import MemeArgsModel, add_meme
from meme_generator.exception import TextOrNameNotEnough, TextOverLength

img_dir = Path(__file__).parent / "images"


def make_friend(images: List[BuildImage], texts: List[str], args: MemeArgsModel):
    img = images[0].convert("RGBA")

    if not texts and not args.user_infos:
        raise TextOrNameNotEnough("make_friend")
    name = texts[0] if texts else args.user_infos[0].name

    bg = BuildImage.open(img_dir / "0.png")
    frame = img.resize_width(1000)
    frame.paste(
        img.resize_width(250).rotate(9, expand=True),
        (743, frame.height - 155),
        alpha=True,
    )
    frame.paste(
        img.square().resize((55, 55)).rotate(9, expand=True),
        (836, frame.height - 278),
        alpha=True,
    )
    frame.paste(bg, (0, frame.height - 1000), alpha=True)

    text_img = Text2Image.from_text(name, 20, fill="white").to_image()
    if text_img.width > 230:
        raise TextOverLength(name)

    text_img = BuildImage(text_img).rotate(9, expand=True)
    frame.paste(text_img, (710, frame.height - 308), alpha=True)
    return frame.save_jpg()


add_meme(
    "make_friend",
    make_friend,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    keywords=["交个朋友"],
)
