from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import MemeArgsModel, add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def stew(images: list[BuildImage], texts: list[str], args: MemeArgsModel):
    name = texts[0] if texts else args.user_infos[0].name if args.user_infos else "群友"
    text = f"生活不易,炖{name}出气"

    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (2, frame.height - 30, frame.width - 2, frame.height),
            text,
            max_fontsize=30,
            min_fontsize=6,
            lines_align="center",
        )
    except ValueError:
        raise TextOverLength(name)

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize((181, 154), keep_ratio=True)
        return frame.copy().paste(img, (9, -2), below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "stew",
    stew,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    keywords=["炖"],
    date_created=datetime(2024, 1, 19),
    date_modified=datetime(2024, 1, 19),
)
