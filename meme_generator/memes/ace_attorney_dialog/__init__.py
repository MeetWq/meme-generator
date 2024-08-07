import math
from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage, Text2Image

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def ace_attorney_dialog(images, texts: list[str], args):
    def shadow_text(text: str, fontsize: int) -> BuildImage:
        fontname = "PangMenZhengDao-Cu"
        inner = Text2Image.from_text(
            text,
            fontsize,
            fill="#e60012",
            fontname=fontname,
            stroke_width=4,
            stroke_fill="#500000",
        ).to_image()
        shadow_width = 10
        shadow = Text2Image.from_text(
            text,
            fontsize,
            fill="#500000",
            fontname=fontname,
            stroke_width=shadow_width,
            stroke_fill="#500000",
        ).to_image()
        dy = 30
        dx = 15
        img = BuildImage.new(
            "RGBA", (inner.width + dx + shadow_width, inner.height + dy + shadow_width)
        )
        img.paste(shadow, (dx - shadow_width, dy - shadow_width), alpha=True)
        img.paste(inner, (0, 0), alpha=True)
        return img

    text = texts[0]
    text_imgs: list[BuildImage] = []
    for char in text:
        text_imgs.append(shadow_text(char, 650))

    total_width = sum(img.width for img in text_imgs)
    if total_width > 4000:
        raise TextOverLength(text)

    def combine_text(text_imgs: list[BuildImage]) -> BuildImage:
        ratio = 0.4
        text_w = sum(img.width for img in text_imgs) - sum(
            round(img.width * ratio) for img in text_imgs[1:]
        )
        text_h = max(img.height for img in text_imgs)
        text_img = BuildImage.new("RGBA", (text_w, text_h))
        x = 0
        for img in text_imgs:
            text_img.paste(img, (x, round((text_h - img.height) / 2)), alpha=True)
            x += img.width - round(img.width * ratio)
        return text_img

    frame = BuildImage.open(img_dir / "bubble.png")
    mark = BuildImage.open(img_dir / "mark.png")

    if total_width <= 2000:
        text_img = combine_text(text_imgs)
        max_width = 900
        if total_width > max_width:
            text_img = text_img.resize(
                (max_width, round(max_width / text_img.width * text_img.height))
            )
        text_img = text_img.rotate(10, expand=True)
        frame.paste(
            text_img,
            (
                round((frame.width - text_img.width) / 2),
                round((frame.height - text_img.height) / 2),
            ),
            alpha=True,
        )
        frame.paste(mark, (630, 230), alpha=True)

    else:
        index = math.ceil(len(text_imgs) / 2)
        text_img1 = combine_text(text_imgs[:index])
        text_img2 = combine_text(text_imgs[index:])
        ratio = 0.6
        text_img1 = text_img1.resize(
            (round(text_img1.width * ratio), round(text_img1.height * ratio))
        )
        text_img2 = text_img2.resize(
            (round(text_img2.width * ratio), round(text_img2.height * ratio))
        )
        text_img1 = text_img1.rotate(10, expand=True)
        text_img2 = text_img2.rotate(10, expand=True)
        frame.paste(
            text_img1,
            (round((frame.width - text_img1.width) / 2) - 50, 775 - text_img1.height),
            alpha=True,
        )
        frame.paste(
            text_img2,
            (round((frame.width - text_img2.width) / 2) + 50, 325),
            alpha=True,
        )
        frame.paste(mark, (680, 320), alpha=True)

    return frame.save_png()


add_meme(
    "ace_attorney_dialog",
    ace_attorney_dialog,
    min_texts=1,
    max_texts=1,
    default_texts=["表情包制作"],
    keywords=["逆转裁判气泡"],
    date_created=datetime(2024, 5, 3),
    date_modified=datetime(2024, 5, 3),
)
