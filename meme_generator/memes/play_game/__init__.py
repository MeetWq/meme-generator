from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"

default_text = "来玩休闲游戏啊"


def play_game(images: list[BuildImage], texts: list[str], args):
    text = texts[0] if texts else default_text
    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (20, frame.height - 70, frame.width - 20, frame.height),
            text,
            max_fontsize=40,
            min_fontsize=25,
            stroke_fill="white",
            stroke_ratio=0.06,
        )
    except ValueError:
        raise TextOverLength(text)

    def make(imgs: list[BuildImage]) -> BuildImage:
        points = ((0, 5), (227, 0), (216, 150), (0, 165))
        screen = (
            imgs[0]
            .convert("RGBA")
            .resize((220, 160), keep_ratio=True)
            .perspective(points)
        )
        return frame.copy().paste(screen.rotate(9, expand=True), (161, 117), below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "play_game",
    play_game,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=[default_text],
    keywords=["玩游戏"],
    date_created=datetime(2022, 1, 4),
    date_modified=datetime(2023, 2, 14),
)
