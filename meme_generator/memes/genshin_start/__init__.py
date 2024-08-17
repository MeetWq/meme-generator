from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import CommandShortcut, add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def genshin_start(images: list[BuildImage], texts: list[str], args):
    frame = BuildImage.open(img_dir / "0.png")
    if texts:
        text = texts[0]
        try:
            frame.draw_text(
                (100, frame.height - 150, frame.width - 100, frame.height),
                text,
                max_fontsize=100,
                min_fontsize=70,
                fill="white",
                stroke_fill="black",
                stroke_ratio=0.05,
            )
        except ValueError:
            raise TextOverLength(text)

    def make(imgs: list[BuildImage]) -> BuildImage:
        points = ((0, 116), (585, 0), (584, 319), (43, 385))
        screen = (
            imgs[0]
            .convert("RGBA")
            .resize((600, 330), keep_ratio=True)
            .perspective(points)
        )
        return frame.copy().paste(screen, (412, 121), below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "genshin_start",
    genshin_start,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=["原神，启动！"],
    keywords=["原神启动"],
    shortcuts=[
        CommandShortcut(
            key=r"(?P<text>\S+启动[!！]?)",
            args=["{text}"],
            humanized="xx启动",
        )
    ],
    date_created=datetime(2023, 7, 1),
    date_modified=datetime(2023, 7, 1),
)
