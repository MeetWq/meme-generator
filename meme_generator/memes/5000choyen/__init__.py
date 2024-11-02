from datetime import datetime

from PIL.Image import Image as IMG
from PIL.Image import Resampling, Transform
from pil_utils import BuildImage, Text2Image
from pil_utils.gradient import ColorStop, LinearGradient

from meme_generator import add_meme


def fivethousand_choyen(images, texts: list[str], args):
    fontsize = 200
    font_families = ["Noto Sans SC"]
    text = texts[0]
    pos_x = 20
    pos_y = 0
    imgs: list[tuple[IMG, tuple[int, int]]] = []

    def transform(img: IMG) -> IMG:
        skew = 0.45
        dw = round(img.height * skew)
        return img.transform(
            (img.width + dw, img.height),
            Transform.AFFINE,
            (1, skew, -dw, 0, 1, 0),
            Resampling.BILINEAR,
        )

    def add_color_text(stroke_width: int, fill: str, pos: tuple[int, int]):
        t2m = Text2Image.from_text(
            text,
            fontsize,
            font_families=font_families,
            fill=fill,
            stroke_width=stroke_width,
            stroke_fill=fill,
        )
        imgs.append(
            (transform(t2m.to_image(padding=(20, 0))), (pos_x + pos[0], pos_y + pos[1]))
        )

    def add_gradient_text(
        stroke_width: int,
        dir: tuple[int, int, int, int],
        color_stops: list[tuple[float, tuple[int, int, int]]],
        pos: tuple[int, int],
    ):
        gradient = LinearGradient(
            (dir[0] - pos_x, dir[1] - pos_y, dir[2] - pos_x, dir[3] - pos_y),
            [ColorStop(*color_stop) for color_stop in color_stops],
        )
        paint = gradient.create_paint()
        t2m = Text2Image.from_text(
            text,
            fontsize,
            font_families=font_families,
            fill=paint,
            stroke_width=stroke_width,
            stroke_fill=paint,
        )
        imgs.append(
            (transform(t2m.to_image(padding=(20, 0))), (pos_x + pos[0], pos_y + pos[1]))
        )

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
    font_families = ["Noto Serif SC"]
    pos_x = 280
    pos_y = 260
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
    date_created=datetime(2022, 10, 29),
    date_modified=datetime(2024, 11, 2),
)
