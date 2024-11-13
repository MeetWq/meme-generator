from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def dont_press(images, texts: list[str], args):
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
        )
    except ValueError:
        raise TextOverLength(text)
    return frame.save_jpg()


add_meme(
    "dont_press",
    dont_press,
    min_texts=1,
    max_texts=1,
    default_texts=["世界毁灭"],
    keywords=["不要按"],
)
