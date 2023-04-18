from pathlib import Path
from typing import List, Literal, Tuple

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def wujing(images, texts: List[str], args):
    frame = BuildImage.open(img_dir / "0.jpg")

    def draw(
        pos: Tuple[float, float, float, float],
        text: str,
        align: Literal["left", "right", "center"],
    ):
        try:
            frame.draw_text(
                pos,
                text,
                halign=align,
                max_fontsize=100,
                min_fontsize=50,
                fill="white",
                stroke_fill="black",
                stroke_ratio=0.05,
            )
        except ValueError:
            raise TextOverLength(text)

    if texts[0]:
        parts = texts[0].split()
        if len(parts) >= 2:
            draw((50, 430, 887, 550), " ".join(parts[:-1]), "left")
        draw((20, 560, 350, 690), parts[-1], "right")
    if texts[1]:
        parts = texts[1].split()
        draw((610, 540, 917, 670), parts[0], "left")
        if len(parts) >= 2:
            draw((50, 680, 887, 810), " ".join(parts[1:]), "center")

    return frame.save_jpg()


add_meme(
    "wujing",
    wujing,
    min_texts=2,
    max_texts=2,
    default_texts=["不买华为不是", "人"],
    keywords=["吴京xx中国xx"],
    patterns=[r"吴京[\s:：]*(.*?)中国(.*)"],
)
