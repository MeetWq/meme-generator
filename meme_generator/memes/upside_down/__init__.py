from datetime import datetime

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif

default_text = "我看你们是反了！"


def upside_down(images: list[BuildImage], texts: list[str], args):
    text = texts[0] if texts else default_text

    img_w = 500
    text_h = 80
    text_frame = BuildImage.new("RGBA", (img_w, text_h), "white")
    try:
        text_frame.draw_text(
            (20, 0, img_w - 20, text_h),
            text,
            max_fontsize=55,
            min_fontsize=30,
        )
    except ValueError:
        raise TextOverLength(text)

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize_width(img_w).rotate(180)
        img_h = img.height
        frame = BuildImage.new("RGBA", (img_w, img_h + text_h), "white")
        return frame.paste(text_frame, alpha=True).paste(img, (0, text_h), alpha=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "upside_down",
    upside_down,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=[default_text],
    keywords=["反了"],
    date_created=datetime(2024, 10, 12),
    date_modified=datetime(2024, 10, 12),
)
