import random
from pathlib import Path
from typing import List

from pil_utils import BuildImage, Text2Image

from meme_generator import MemeArgsModel, add_meme
from meme_generator.exception import TextOrNameNotEnough, TextOverLength

img_dir = Path(__file__).parent / "images"


def always_like(images: List[BuildImage], texts: List[str], args: MemeArgsModel):
    names = [info.name for info in args.user_infos]

    if len(images) > len(texts) + len(names):
        raise TextOrNameNotEnough("always_like")
    texts = texts + names

    img = images[0].convert("RGBA")
    name = texts[0]
    text = "我永远喜欢" + name

    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(
        img.resize((350, 400), keep_ratio=True, inside=True), (25, 35), alpha=True
    )
    try:
        frame.draw_text(
            (20, 470, frame.width - 20, 570),
            text,
            max_fontsize=70,
            min_fontsize=30,
            weight="bold",
        )
    except ValueError:
        raise TextOverLength(text)

    def random_color():
        return random.choice(
            ["red", "darkorange", "gold", "darkgreen", "blue", "cyan", "purple"]
        )

    if len(images) > 1:
        text_w = Text2Image.from_text(text, 70).width
        ratio = min((frame.width - 40) / text_w, 1)
        text_w *= ratio
        name_w = Text2Image.from_text(name, 70).width * ratio
        start_w = text_w - name_w + (frame.width - text_w) // 2
        frame.draw_line(
            (start_w, 525, start_w + name_w, 525), fill=random_color(), width=10
        )

    current_h = 400
    for i, (image, name) in enumerate(zip(images[1:], texts[1:]), start=1):
        img = image.convert("RGBA")
        frame.paste(
            img.resize((350, 400), keep_ratio=True, inside=True),
            (10 + random.randint(0, 50), 20 + random.randint(0, 70)),
            alpha=True,
        )
        try:
            frame.draw_text(
                (400, current_h, frame.width - 20, current_h + 80),
                name,
                max_fontsize=70,
                min_fontsize=30,
                weight="bold",
            )
        except ValueError:
            raise TextOverLength(text)

        if len(images) > i + 1:
            name_w = min(Text2Image.from_text(name, 70).width, 380)
            start_w = 400 + (410 - name_w) // 2
            line_h = current_h + 40
            frame.draw_line(
                (start_w, line_h, start_w + name_w, line_h),
                fill=random_color(),
                width=10,
            )
        current_h -= 70
    return frame.save_jpg()


add_meme(
    "always_like",
    always_like,
    min_images=1,
    max_images=6,
    min_texts=0,
    max_texts=6,
    keywords=["我永远喜欢"],
)
