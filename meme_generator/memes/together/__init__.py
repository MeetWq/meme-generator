from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import MemeArgsModel, add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"

default_text = "一起玩{name}吧！"


def together(images: list[BuildImage], texts: list[str], args: MemeArgsModel):
    frame = BuildImage.open(img_dir / "0.png")
    name = args.user_infos[0].name if args.user_infos else ""
    text = texts[0] if texts else default_text.format(name=name)
    try:
        frame.draw_text(
            (10, 140, 190, 190),
            text,
            weight="bold",
            max_fontsize=50,
            min_fontsize=10,
            allow_wrap=True,
        )
    except ValueError:
        raise TextOverLength(text)

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize((63, 63), keep_ratio=True)
        return frame.copy().paste(img, (132, 36), alpha=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "together",
    together,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=[default_text],
    keywords=["一起"],
    date_created=datetime(2022, 10, 13),
    date_modified=datetime(2023, 3, 29),
)
