from typing import List, Tuple

from PIL.Image import Image as IMG
from PIL.Image import Resampling, Transform
from pil_utils import BuildImage, Text2Image
from pil_utils.gradient import ColorStop, LinearGradient

from meme_generator import add_meme


def fivethousand_choyen(images, texts: List[str], args):
    fontsize = 200
    fontname = "Noto Sans SC"
    text = texts[0]
    pos_x = 40
    pos_y = 220
    imgs: List[Tuple[IMG, Tuple[int, int]]] = []

    def transform(img: IMG) -> IMG:
        skew = 0.45
        dw = round(img.height * skew)
        return img.transform(
            (img.width + dw, img.height),
            Transform.AFFINE,
            (1, skew, -dw, 0, 1, 0),
            Resampling.BILINEAR,
        )

    def shift(t2m: Text2Image) -> Tuple[int, int]:
        return (
            pos_x
            - t2m.lines[0].chars[0].stroke_width
            - max(char.stroke_width for char in t2m.lines[0].chars),
            pos_y - t2m.lines[0].ascent,
        )

    def add_color_text(stroke_width: int, fill: str, pos: Tuple[int, int]):
        t2m = Text2Image.from_text(
            text, fontsize, fontname=fontname, stroke_width=stroke_width, fill=fill
        )
        dx, dy = shift(t2m)
        imgs.append((transform(t2m.to_image()), (dx + pos[0], dy + pos[1])))

    def add_gradient_text(
        stroke_width: int,
        dir: Tuple[int, int, int, int],
        color_stops: List[Tuple[float, Tuple[int, int, int]]],
        pos: Tuple[int, int],
    ):
        t2m = Text2Image.from_text(
            text, fontsize, fontname=fontname, stroke_width=stroke_width, fill="white"
        )
        mask = transform(t2m.to_image()).convert("L")
        dx, dy = shift(t2m)
        gradient = LinearGradient(
            (dir[0] - dx, dir[1] - dy, dir[2] - dx, dir[3] - dy),
            [ColorStop(*color_stop) for color_stop in color_stops],
        )
        bg = gradient.create_image(mask.size)
        bg.putalpha(mask)
        imgs.append((bg, (dx + pos[0], dy + pos[1])))

    # 黑
    add_color_text(22, "black", (8, 8))
    # 银
    add_gradient_text(
        20,
        (0, 38, 0, 234),
        [
            (0.0, (0, 15, 36)),
            (0.1, (255, 255, 255)),
            (0.18, (55, 58, 59)),
            (0.25, (55, 58, 59)),
            (0.5, (200, 200, 200)),
            (0.75, (55, 58, 59)),
            (0.85, (25, 20, 31)),
            (0.91, (240, 240, 240)),
            (0.95, (166, 175, 194)),
            (1, (50, 50, 50)),
        ],
        (8, 8),
    )
    # 黑
    add_color_text(16, "black", (0, 0))
    # 金
    add_gradient_text(
        10,
        (0, 40, 0, 200),
        [
            (0, (253, 241, 0)),
            (0.25, (245, 253, 187)),
            (0.4, (255, 255, 255)),
            (0.75, (253, 219, 9)),
            (0.9, (127, 53, 0)),
            (1, (243, 196, 11)),
        ],
        (0, 0),
    )
    # 黑
    add_color_text(6, "black", (4, -6))
    # 白
    add_color_text(6, "white", (0, -6))
    # 红
    add_gradient_text(
        4,
        (0, 50, 0, 200),
        [
            (0, (255, 100, 0)),
            (0.5, (123, 0, 0)),
            (0.51, (240, 0, 0)),
            (1, (5, 0, 0)),
        ],
        (0, -6),
    )
    # 红
    add_gradient_text(
        0,
        (0, 50, 0, 200),
        [
            (0, (230, 0, 0)),
            (0.5, (123, 0, 0)),
            (0.51, (240, 0, 0)),
            (1, (5, 0, 0)),
        ],
        (0, -6),
    )

    text = texts[1]
    fontname = "Noto Serif SC"
    pos_x = 300
    pos_y = 480
    # 黑
    add_color_text(22, "black", (10, 4))
    # 银
    add_gradient_text(
        19,
        (0, 320, 0, 506),
        [
            (0, (0, 15, 36)),
            (0.25, (250, 250, 250)),
            (0.5, (150, 150, 150)),
            (0.75, (55, 58, 59)),
            (0.85, (25, 20, 31)),
            (0.91, (240, 240, 240)),
            (0.95, (166, 175, 194)),
            (1, (50, 50, 50)),
        ],
        (10, 4),
    )
    # 黑
    add_color_text(17, "#10193A", (0, 0))
    # 白
    add_color_text(8, "#D0D0D0", (0, 0))
    # 绀
    add_gradient_text(
        7,
        (0, 320, 0, 480),
        [
            (0, (16, 25, 58)),
            (0.03, (255, 255, 255)),
            (0.08, (16, 25, 58)),
            (0.2, (16, 25, 58)),
            (1, (16, 25, 58)),
        ],
        (0, 0),
    )
    # 银
    add_gradient_text(
        0,
        (0, 320, 0, 480),
        [
            (0, (245, 246, 248)),
            (0.15, (255, 255, 255)),
            (0.35, (195, 213, 220)),
            (0.5, (160, 190, 201)),
            (0.51, (160, 190, 201)),
            (0.52, (196, 215, 222)),
            (1.0, (255, 255, 255)),
        ],
        (0, -6),
    )

    img_h = 580
    img_w = max([img.width + pos[0] for img, pos in imgs])
    frame = BuildImage.new("RGBA", (img_w, img_h), "white")
    for img, pos in imgs:
        frame.paste(img, pos, alpha=True)
    return frame.save_jpg()


add_meme(
    "5000choyen",
    fivethousand_choyen,
    min_texts=2,
    max_texts=2,
    default_texts=["我去", "洛天依"],
    keywords=["5000兆"],
)
