from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def luxun_say(images, texts: List[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.jpg")
    try:
        frame.draw_text(
            (40, frame.height - 200, frame.width - 40, frame.height - 100),
            text,
            allow_wrap=True,
            max_fontsize=40,
            min_fontsize=30,
            fill="white",
        )
    except ValueError:
        raise TextOverLength(text)
    frame.draw_text((320, 400), "--鲁迅", fontsize=30, fill="white")
    return frame.save_jpg()


add_meme(
    "luxun_say",
    luxun_say,
    min_texts=1,
    max_texts=1,
    default_texts=["我没有说过这句话"],
    keywords=["鲁迅说", "鲁迅说过"],
)
