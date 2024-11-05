from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def yeshu(images, texts: list[str], args):
    color_yellow = "#feef50"
    color_blue = "#0021fc"
    color_red = "#fd0000"

    frame_w = 600
    frame_h = 1200
    frame = BuildImage.new("RGBA", (frame_w, frame_h), color_yellow)

    padding = 4
    frame.draw_rectangle(
        (padding, padding, frame_w - padding, frame_h - padding), fill="black"
    )

    padding_x = 28
    h1 = 16
    h2 = 1000
    frame.draw_rectangle((padding_x, h1, frame_w - padding_x, h2), fill=color_yellow)

    padding_x = 34
    h1 = 88
    h2 = 999
    frame.draw_rectangle((padding_x, h1, frame_w - padding_x, h2), fill="black")

    padding_x += 2
    h1 += 2
    h2 -= 2
    frame.draw_rectangle((padding_x, h1, frame_w - padding_x, h2), fill=color_blue)

    h1 = 16
    h2 = 88
    try:
        frame.draw_text(
            (padding_x, h1, frame_w - padding_x, h2),
            texts[0],
            max_fontsize=70,
            min_fontsize=40,
            fill="black",
            font_style="bold",
        )
    except ValueError:
        raise TextOverLength(texts[0])

    h1 = 90
    h2 = 170
    try:
        frame.draw_text(
            (padding_x, h1, frame_w - padding_x, h2),
            texts[1],
            max_fontsize=70,
            min_fontsize=40,
            fill="white",
            font_style="bold",
        )
    except ValueError:
        raise TextOverLength(texts[1])

    h1 = 390
    h2 = 590
    try:
        frame.draw_text(
            (padding_x, h1, frame_w - padding_x, h2),
            texts[3],
            max_fontsize=200,
            min_fontsize=100,
            fill="white",
            font_style="bold",
            stroke_fill="black",
            stroke_ratio=0.025,
        )
    except ValueError:
        raise TextOverLength(texts[3])

    h1 = 580
    h2 = 660
    try:
        frame.draw_text(
            (padding_x, h1, frame_w - padding_x, h2),
            texts[4],
            max_fontsize=70,
            min_fontsize=40,
            fill=color_yellow,
            font_style="bold",
        )
    except ValueError:
        raise TextOverLength(texts[4])

    h1 = 740
    h2 = 1000
    try:
        frame.draw_text(
            (padding_x, h1, frame_w - padding_x, h2),
            texts[6],
            max_fontsize=250,
            min_fontsize=150,
            fill=color_yellow,
            font_style="bold",
            stroke_fill="black",
            stroke_ratio=0.025,
        )
    except ValueError:
        raise TextOverLength(texts[6])

    padding_x = 38
    h1 = 170
    h2 = 403
    rrect = BuildImage.new(
        "RGBA", (frame_w - padding_x * 2, h2 - h1), color_yellow
    ).circle_corner(30)
    frame.alpha_composite(rrect, (padding_x, h1))

    padding_x += 3
    h1 += 3
    h2 -= 3
    rrect = BuildImage.new(
        "RGBA", (frame_w - padding_x * 2, h2 - h1), color_red
    ).circle_corner(28)
    frame.alpha_composite(rrect, (padding_x, h1))

    padding_x += 10
    h1 -= 15
    try:
        frame.draw_text(
            (padding_x, h1, frame_w - padding_x, h2),
            texts[2],
            max_fontsize=230,
            min_fontsize=100,
            fill="white",
            font_style="bold",
        )
    except ValueError:
        raise TextOverLength(texts[2])

    padding_x = 32
    h1 = 668
    h2 = 760
    rrect = BuildImage.new(
        "RGBA", (frame_w - padding_x * 2, h2 - h1), color_red
    ).circle_corner(5)
    frame.alpha_composite(rrect, (padding_x, h1))

    padding_x += 4
    h1 += 4
    h2 -= 4
    rrect = BuildImage.new(
        "RGBA", (frame_w - padding_x * 2, h2 - h1), color_yellow
    ).circle_corner(1)
    frame.alpha_composite(rrect, (padding_x, h1))

    h1 -= 5
    try:
        frame.draw_text(
            (padding_x, h1, frame_w - padding_x, h2),
            texts[5],
            max_fontsize=100,
            min_fontsize=50,
            fill=color_red,
            font_style="bold",
        )
    except ValueError:
        raise TextOverLength(texts[5])

    padding_x = 10
    h1 = 1000
    h2 = 1188
    rrect = BuildImage.new(
        "RGBA", (frame_w - padding_x * 2, h2 - h1), color_yellow
    ).circle_corner(8)
    frame.alpha_composite(rrect, (padding_x, h1))

    padding_x += 2
    h1 += 2
    h2 -= 2
    rrect = BuildImage.new(
        "RGBA", (frame_w - padding_x * 2, h2 - h1), color_red
    ).circle_corner(6)
    frame.alpha_composite(rrect, (padding_x, h1))

    padding_x += 10
    h1 -= 10
    try:
        frame.draw_text(
            (padding_x, h1, frame_w - padding_x, h2),
            texts[7],
            max_fontsize=180,
            min_fontsize=50,
            allow_wrap=True,
            lines_align="center",
            fill="white",
            font_style="bold",
        )
    except ValueError:
        raise TextOverLength(texts[7])

    return frame.save_png()


add_meme(
    "yeshu",
    yeshu,
    min_texts=8,
    max_texts=8,
    default_texts=[
        "椰子特产在海南",
        "正宗",
        "椰树",
        "29年",
        "坚持在海南岛",
        "用新鲜椰子肉",
        "鲜榨",
        "不用椰浆\n不加香精当生榨",
    ],
    keywords=["椰树椰汁"],
    date_created=datetime(2024, 11, 5),
    date_modified=datetime(2024, 11, 5),
)
