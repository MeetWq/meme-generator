from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def meteor(images, texts: List[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (220, 230, 920, 315),
            text,
            allow_wrap=True,
            max_fontsize=80,
            min_fontsize=20,
            fill="white",
        )
    except ValueError:
        raise TextOverLength(text)
    return frame.save_jpg()


add_meme(
    "meteor", meteor, min_texts=1, max_texts=1, default_texts=["我要对象"], keywords=["流星"]
)
