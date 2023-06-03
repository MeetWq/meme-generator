from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import MemeArgsModel, add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def fill_head(images: List[BuildImage], texts: List[str], args: MemeArgsModel):
    name = texts[0] if texts else (args.user_infos[0].name if args.user_infos else "它")
    text = f"满脑子都是{name}"
    frame = BuildImage.open(img_dir / "0.jpg")
    try:
        frame.draw_text(
            (20, 458, frame.width - 20, 550), text, max_fontsize=65, min_fontsize=30
        )
    except:
        raise TextOverLength(name)

    def make(img: BuildImage) -> BuildImage:
        img = img.convert("RGBA").resize((210, 170), keep_ratio=True, inside=True)
        return frame.copy().paste(img, (150, 2), alpha=True)

    return make_jpg_or_gif(images[0], make)


add_meme(
    "fill_head",
    fill_head,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    keywords=["满脑子"],
    patterns=[r"满脑子都是(\S+)"],
)
