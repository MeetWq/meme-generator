from pathlib import Path

from meme_generator import add_meme
from pil_utils import BuildImage
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def my_opinion(images, texts: list[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (37, 660, 487, 1070),
            text,
            max_fontsize=500,
            min_fontsize=20,
            weight="bold",
        )
    except ValueError:
        raise TextOverLength(text)
    return frame.save_png()


add_meme(
    "my_opinion",
    my_opinion,
    min_texts=1,
    max_texts=1,
    keywords=["我的意见如下", "我的意见是"],
)
