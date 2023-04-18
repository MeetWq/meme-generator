from pathlib import Path
from typing import List, Tuple

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def high_EQ(images, texts: List[str], args):
    frame = BuildImage.open(img_dir / "0.jpg")

    def draw(pos: Tuple[float, float, float, float], text: str):
        try:
            frame.draw_text(
                pos,
                text,
                max_fontsize=100,
                min_fontsize=50,
                allow_wrap=True,
                fill="white",
                stroke_fill="black",
                stroke_ratio=0.05,
            )
        except ValueError:
            raise TextOverLength(text)

    draw((40, 540, 602, 1140), texts[0])
    draw((682, 540, 1244, 1140), texts[1])
    return frame.save_jpg()


add_meme(
    "high_EQ",
    high_EQ,
    min_texts=2,
    max_texts=2,
    default_texts=["高情商", "低情商"],
    keywords=["低情商xx高情商xx"],
    patterns=[r"低情商[\s:：]*(.+?)\s+高情商[\s:：]*(.+)"],
)
