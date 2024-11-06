from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def nopress(images, texts: list[str], args):
    text = texts[0]

    img_path = img_dir / "0.png"
    frame = BuildImage.open(img_path)

    try:
        frame.draw_text(
            (60, 170, 200, 225),
            text,
            allow_wrap=True,
            lines_align="center",
            min_fontsize=20,
            max_fontsize=50,
            fill=(0, 0, 0),
        )
    except ValueError:
        raise TextOverLength(text)
    return frame.save_png()


add_meme(
    "nopress",
    nopress,
    min_texts=0,
    max_texts=1,
    default_texts=["楼上是小南梁"],
    keywords=["不要按"],
)
