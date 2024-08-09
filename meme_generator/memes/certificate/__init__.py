from datetime import datetime
from pathlib import Path

import dateparser
from pil_utils import BuildImage
from pydantic import Field

from meme_generator import (
    MemeArgsModel,
    MemeArgsType,
    ParserArg,
    ParserOption,
    add_meme,
)
from meme_generator.exception import TextOverLength


class Model(MemeArgsModel):
    time: str = Field("", description="指定时间")


args_type = MemeArgsType(
    args_model=Model,
    parser_options=[
        ParserOption(
            names=["-t", "--time"],
            args=[ParserArg(name="time", value="str")],
            help_text="指定时间",
        ),
    ],
)


img_dir = Path(__file__).parent / "images"


def certificate(images, texts: list[str], args: Model):
    time = datetime.now()
    if args.time and (parsed_time := dateparser.parse(args.time)):
        time = parsed_time

    frame = BuildImage.open(img_dir / "0.png")

    try:
        frame.draw_text(
            (340, 660, 770, 800),
            texts[0],
            allow_wrap=False,
            max_fontsize=80,
            min_fontsize=20,
        )
    except ValueError:
        raise TextOverLength(texts[0])
    try:
        frame.draw_text(
            (565, 1040, 2100, 1320),
            texts[1],
            fill="red",
            allow_wrap=True,
            max_fontsize=120,
            min_fontsize=60,
        )
    except ValueError:
        raise TextOverLength(texts[1])
    try:
        frame.draw_text(
            (1500, 1400, 2020, 1520),
            texts[2],
            allow_wrap=False,
            max_fontsize=60,
            min_fontsize=20,
        )
    except ValueError:
        raise TextOverLength(texts[2])
    try:
        frame.draw_text(
            (450, 850, 2270, 1080),
            texts[3]
            if len(texts) >= 4
            else "　　在本学年第一学期中表现优秀，被我校决定评为",
            allow_wrap=True,
            max_fontsize=80,
            min_fontsize=40,
            halign="left",
            valign="top",
        )
    except ValueError:
        raise TextOverLength(texts[3])

    frame.draw_text(
        (1565, 1525, 1700, 1600),
        f"{time.year:04d}",
        allow_wrap=False,
        max_fontsize=60,
        min_fontsize=40,
    )
    frame.draw_text(
        (1752, 1525, 1816, 1600),
        f"{time.month:02d}",
        allow_wrap=False,
        max_fontsize=60,
        min_fontsize=40,
    )
    frame.draw_text(
        (1865, 1525, 1930, 1600),
        f"{time.day:02d}",
        allow_wrap=False,
        max_fontsize=60,
        min_fontsize=40,
    )

    return frame.save_png()


add_meme(
    "certificate",
    certificate,
    min_texts=3,
    max_texts=4,
    default_texts=["小王", "优秀学生", "一年一班"],
    args_type=args_type,
    keywords=["奖状", "证书"],
    date_created=datetime(2023, 12, 3),
    date_modified=datetime(2023, 12, 3),
)
