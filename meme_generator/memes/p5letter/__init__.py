import random
from datetime import datetime
from enum import Enum
from pathlib import Path

from pil_utils import BuildImage, Text2Image

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


class CharMode(Enum):
    FIRST = 1
    WHITE = 2
    RED = 3


class Colors:
    RED = "#E5191C"
    WHITE = "#FDFDFD"
    BLACK = "#0F0F0F"


class BoxChar:
    def __init__(self, char: str, mode: CharMode, font_size: int = 120):
        self.char = char
        self.mode = mode

        self.angle = round(10 * random.random())
        if mode == CharMode.FIRST:
            scale = 1.1
        else:
            scale = 1 - random.choice([0, 1, 2]) / 10
            self.angle *= random.choice([-1, 1])
        self.font_size = font_size * scale

        self.color = Colors.WHITE
        if mode == CharMode.RED:
            self.color = Colors.RED

    def draw(self):
        text_img = Text2Image.from_text(
            self.char, self.font_size, fill=self.color, font_style="bold"
        ).to_image()
        bg_w_scale = 1.4
        bg_h_scale = 1.1
        bg_color = Colors.RED if self.mode == CharMode.FIRST else Colors.BLACK
        bg = BuildImage.new(
            "RGBA",
            (round(text_img.width * bg_w_scale), round(text_img.height * bg_h_scale)),
            bg_color,
        )

        if self.mode == CharMode.FIRST:
            extra_bg_scale = 1.2
            extra_bg = BuildImage.new(
                "RGBA",
                (round(bg.width * extra_bg_scale), round(bg.height * extra_bg_scale)),
                Colors.BLACK,
            )
            extra_angle = round(5 * random.random()) * random.choice([-1, 1])
            bg = bg.rotate(extra_angle, expand=True)
            extra_bg.paste(
                bg,
                ((extra_bg.width - bg.width) // 2, (extra_bg.height - bg.height) // 2),
                alpha=True,
            )
            bg = extra_bg

        border_size = 6
        border = BuildImage.new(
            "RGBA",
            (bg.width + border_size * 2, bg.height + border_size * 2),
            Colors.WHITE,
        )
        border.paste(bg, (border_size, border_size))
        border.paste(
            text_img,
            (
                (border.width - text_img.width) // 2,
                (border.height - text_img.height) // 2,
            ),
            alpha=True,
        )
        self.width = border.width
        self.height = border.height
        result = border.rotate(self.angle, expand=True)
        self.outter_width = result.width
        self.outter_height = result.height
        self.image = result


def p5letter(images, texts: list[str], args):
    text = texts[0]
    lines = text.splitlines()
    if len(lines) > 5:
        raise TextOverLength(text)

    line_images: list[BuildImage] = []
    for line in lines:
        box_chars: list[BoxChar] = []
        for char in line:
            if not char.strip():
                continue
            if not box_chars:
                box_char = BoxChar(char, CharMode.FIRST)
            else:
                box_char = BoxChar(
                    char, CharMode.RED if random.random() < 0.4 else CharMode.WHITE
                )
            box_char.draw()
            box_chars.append(box_char)
        if not box_chars:
            continue
        line_width = (
            sum(box_char.width for box_char in box_chars)
            + (box_chars[0].outter_width - box_chars[0].width) // 2
            + (box_chars[-1].outter_width - box_chars[-1].width) // 2
        )
        if line_width > 1700:
            raise TextOverLength(text)
        line_height = max(box_char.outter_height for box_char in box_chars)
        line_image = BuildImage.new("RGBA", (line_width, line_height))
        x = (box_chars[0].outter_width - box_chars[0].width) // 2
        for box_char in box_chars:
            line_image.paste(
                box_char.image,
                (
                    x - (box_char.outter_width - box_char.width) // 2,
                    (line_height - box_char.outter_height) // 2,
                ),
                alpha=True,
            )
            x += box_char.width
        line_images.append(line_image)

    frame = BuildImage.open(img_dir / "background.png")
    total_height = sum(line_image.height for line_image in line_images)
    y = (frame.height - total_height) // 2
    for line_image in line_images:
        frame.paste(line_image, ((frame.width - line_image.width) // 2, y), alpha=True)
        y += line_image.height

    return frame.save_png()


add_meme(
    "p5letter",
    p5letter,
    min_texts=1,
    max_texts=1,
    default_texts=["TAKEYOURHEART"],
    keywords=["女神异闻录5预告信", "P5预告信"],
    date_created=datetime(2024, 11, 13),
    date_modified=datetime(2024, 11, 13),
)
