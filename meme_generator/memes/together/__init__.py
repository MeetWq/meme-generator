from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import MemeArgsModel, add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def together(images: List[BuildImage], texts: List[str], args: MemeArgsModel):
    frame = BuildImage.open(img_dir / "0.png")
    name = args.user_infos[0].name if args.user_infos else ""
    text = texts[0] if texts else f"一起玩{name}吧！"
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

    def make(img: BuildImage) -> BuildImage:
        img = img.convert("RGBA").resize((63, 63), keep_ratio=True)
        return frame.copy().paste(img, (132, 36), alpha=True)

    return make_jpg_or_gif(images[0], make)


add_meme(
    "together",
    together,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    keywords=["一起"],
)
