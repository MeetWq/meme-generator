from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import CommandShortcut, add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def high_EQ(images, texts: list[str], args):
    frame = BuildImage.open(img_dir / "0.jpg")

    def draw(pos: tuple[float, float, float, float], text: str):
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
    keywords=["高低情商", "低高情商"],
    shortcuts=[
        CommandShortcut(
            key=r"低情商[\s:：]*(?P<low>\S+)\s*高情商[\s:：]*(?P<high>\S+)",
            args=["{low}", "{high}"],
            humanized="低情商xx高情商xx",
        ),
        CommandShortcut(
            key=r"高情商[\s:：]*(?P<high>\S+)\s*低情商[\s:：]*(?P<low>\S+)",
            args=["{low}", "{high}"],
            humanized="高情商xx低情商xx",
        ),
    ],
    date_created=datetime(2022, 6, 12),
    date_modified=datetime(2024, 8, 12),
)
