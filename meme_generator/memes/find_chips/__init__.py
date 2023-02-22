from pathlib import Path
from typing import List, Tuple
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength


img_dir = Path(__file__).parent / "images"


def find_chips(images, texts: List[str], args):
    frame = BuildImage.open(img_dir / "0.jpg")

    def draw(pos: Tuple[float, float, float, float], text: str):
        try:
            frame.draw_text(
                pos, text, max_fontsize=40, min_fontsize=20, allow_wrap=True
            )
        except ValueError:
            raise TextOverLength(text)

    draw((405, 54, 530, 130), texts[0])
    draw((570, 62, 667, 160), texts[1])
    draw((65, 400, 325, 463), texts[2])
    draw((430, 400, 630, 470), texts[3])
    return frame.save_jpg()


add_meme(
    "find_chips",
    find_chips,
    min_texts=4,
    max_texts=4,
    default_texts=[
        "我们要飞向何方",
        "我打算待会去码头整点薯条",
        "你误会我了伙计，我说的是咱们这一辈子的终极目标。归根结底，活着是为了什么",
        "为了待会去码头整点薯条",
    ],
    keywords=["整点薯条"],
)
