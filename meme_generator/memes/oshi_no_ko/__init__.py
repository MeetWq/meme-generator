from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage, Text2Image

from meme_generator import CommandShortcut, add_meme
from meme_generator.exception import TextOverLength
from meme_generator.tags import MemeTags
from meme_generator.utils import make_png_or_gif

img_dir = Path(__file__).parent / "images"


def oshi_no_ko(images: list[BuildImage], texts: list[str], args):
    name = texts[0] if texts else "网友"

    text_frame1 = BuildImage.open(img_dir / "text1.png")
    text_frame2 = BuildImage.open(img_dir / "text2.png")

    bias_y = 5
    text_frame3 = BuildImage(
        Text2Image.from_text(
            name,
            fontname="HiraginoMin",
            fontsize=150,
            stroke_width=4,
            stroke_fill="white",
        ).to_image()
    ).resize_height(text_frame1.height + bias_y)
    if text_frame3.width > 800:
        raise TextOverLength(name)

    text_frame = BuildImage.new(
        "RGBA",
        (text_frame1.width + text_frame2.width + text_frame3.width, text_frame2.height),
    )
    text_frame.paste(text_frame1, (0, 0), alpha=True).paste(
        text_frame3, (text_frame1.width, bias_y), alpha=True
    ).paste(text_frame2, (text_frame1.width + text_frame3.width, 0), alpha=True)
    text_frame = text_frame.resize_width(663)

    background = BuildImage.open(img_dir / "background.png")
    foreground = BuildImage.open(img_dir / "foreground.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize((681, 692), keep_ratio=True)
        return (
            background.copy()
            .paste(img, alpha=True)
            .paste(text_frame, (9, 102 - text_frame.height // 2), alpha=True)
            .paste(foreground, alpha=True)
        )

    return make_png_or_gif(images, make)


add_meme(
    "oshi_no_ko",
    oshi_no_ko,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=["网友"],
    keywords=["我推的网友"],
    shortcuts=[
        CommandShortcut(
            key=r"我推的(?P<name>\S+)",
            args=["{name}"],
            humanized="我推的xx",
        )
    ],
    tags=MemeTags.oshi_no_ko,
    date_created=datetime(2023, 6, 1),
    date_modified=datetime(2023, 6, 23),
)
