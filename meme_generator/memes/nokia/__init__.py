from pathlib import Path
from typing import List

from pil_utils import BuildImage, Text2Image

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def nokia(images, texts: List[str], args):
    text = texts[0][:900]
    text_img = (
        Text2Image.from_text(text, 70, fontname="FZXS14", fill="black", spacing=30)
        .wrap(700)
        .to_image()
    )
    text_img = (
        BuildImage(text_img)
        .resize_canvas((700, 450), direction="northwest")
        .rotate(-9.3, expand=True)
    )

    head_img = Text2Image.from_text(
        f"{len(text)}/900", 70, fontname="FZXS14", fill=(129, 212, 250, 255)
    ).to_image()
    head_img = BuildImage(head_img).rotate(-9.3, expand=True)

    frame = BuildImage.open(img_dir / "0.jpg")
    frame.paste(text_img, (205, 330), alpha=True)
    frame.paste(head_img, (790, 320), alpha=True)
    return frame.save_jpg()


add_meme(
    "nokia",
    nokia,
    min_texts=1,
    max_texts=1,
    default_texts=["无内鬼，继续交易"],
    keywords=["诺基亚", "有内鬼"],
)
