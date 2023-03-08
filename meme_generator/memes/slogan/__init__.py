from pathlib import Path
from typing import List, Tuple

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def slogan(images, texts: List[str], args):
    frame = BuildImage.open(img_dir / "0.jpg")

    def draw(pos: Tuple[float, float, float, float], text: str):
        try:
            frame.draw_text(
                pos, text, max_fontsize=40, min_fontsize=15, allow_wrap=True
            )
        except ValueError:
            raise TextOverLength(text)

    draw((10, 0, 294, 50), texts[0])
    draw((316, 0, 602, 50), texts[1])
    draw((10, 230, 294, 280), texts[2])
    draw((316, 230, 602, 280), texts[3])
    draw((10, 455, 294, 505), texts[4])
    draw((316, 455, 602, 505), texts[5])

    return frame.save_jpg()


add_meme(
    "slogan",
    slogan,
    min_texts=6,
    max_texts=6,
    default_texts=["我们是谁？", "浙大人！", "到浙大来做什么？", "混！", "将来毕业后要做什么样的人？", "混混！"],
    keywords=["口号"],
)
