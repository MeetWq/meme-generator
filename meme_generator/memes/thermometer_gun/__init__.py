from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_png_or_gif

img_dir = Path(__file__).parent / "images"

defalut_text = "笨蛋"


def thermometer_gun(images: list[BuildImage], texts: list[str], args):
    text = defalut_text if not len(texts) else texts[0]
    text_frame = BuildImage.new("RGBA", (200, 125))
    try:
        text_frame.draw_text(
            (0, 0, 200, 125),
            text,
            allow_wrap=True,
            max_fontsize=60,
            min_fontsize=15,
            fontname="FZKaTong-M19S",
            lines_align="center",
        )
    except ValueError:
        raise TextOverLength(text)
    img_w, img_h = images[0].size
    if img_w > img_h:
        size = (round(img_h), round(img_h))
        pos = (round(img_w - img_h), 0)
    else:
        size = (round(img_w), round(img_w))
        pos = (0, round(img_h - img_w))
    frame = (
        BuildImage.open(img_dir / "0.png")
        .paste(text_frame, (555, 240), alpha=True)
        .resize(size)
    )

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA")
        return img.paste(frame, pos, alpha=True)

    return make_png_or_gif(images, make)


add_meme(
    "thermometer_gun",
    thermometer_gun,
    min_images=1,
    max_images=1,
    max_texts=1,
    min_texts=0,
    keywords=["体温枪"],
    default_texts=[defalut_text],
    date_created=datetime(2024, 9, 3),
    date_modified=datetime(2024, 9, 3),
)
