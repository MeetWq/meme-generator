from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def capoo_say(images, texts: List[str], args):
    text = texts[0]
    text_frame = BuildImage.new("RGBA", (80, 80))
    try:
        text_frame.draw_text(
            (0, 0, 80, 80),
            text,
            max_fontsize=80,
            min_fontsize=30,
            allow_wrap=True,
            fontname="FZKaTong-M19S",
        )
    except ValueError:
        raise TextOverLength(text)

    params = [
        (80, 80, 43, 30, 0),
        (78, 78, 44, 30, 0),
        (78, 78, 44, 29, 0),
        None,
        None,
        None,
        None,
        (45, 45, 74, 112, 25),
        (73, 73, 41, 42, 17),
        (80, 80, 43, 36, 0),
    ]

    frames: List[IMG] = []
    for i in range(10):
        frame = BuildImage.open(img_dir / f"{i}.png")
        param = params[i]
        if param:
            x, y, w, h, angle = param
            frame.paste(
                text_frame.resize((x, y)).rotate(angle, expand=True), (w, h), alpha=True
            )
        frames.append(frame.image)
    return save_gif(frames, 0.11)


add_meme(
    "capoo_say",
    capoo_say,
    min_texts=1,
    max_texts=1,
    default_texts=["寄"],
    keywords=["咖波说"],
)
