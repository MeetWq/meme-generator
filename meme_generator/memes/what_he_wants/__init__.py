from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def what_he_wants(images: List[BuildImage], texts: List[str], args):
    date = texts[0] if texts else "今年520"
    text = f"{date}我会给你每个男人都最想要的东西···"
    frame = BuildImage.open(img_dir / "0.png")

    def make(img: BuildImage) -> BuildImage:
        img = img.convert("RGBA").resize((538, 538), keep_ratio=True, inside=True)
        new_frame = frame.copy()
        try:
            new_frame.draw_text(
                (0, 514, 1024, 614),
                text,
                fill="black",
                max_fontsize=80,
                min_fontsize=20,
                stroke_ratio=0.07,
                stroke_fill="white",
                weight="bold",
                valign="bottom",
            )
        except ValueError:
            raise TextOverLength(date)
        new_frame.paste(img, (486, 616), alpha=True)
        return new_frame

    return make_jpg_or_gif(images[0], make)


add_meme(
    "what_he_wants",
    what_he_wants,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=["今年520"],
    keywords=["最想要的东西"],
)
