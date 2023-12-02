from datetime import datetime
from pathlib import Path
from typing import List

import dateparser
from pil_utils import BuildImage
from pydantic import Field

from meme_generator import MemeArgsModel, MemeArgsParser, MemeArgsType, add_meme
from meme_generator.exception import TextOverLength

parser = MemeArgsParser()
parser.add_argument("-t", "--time", type=str, default="", help="指定时间")


class Model(MemeArgsModel):
    time: str = Field("", description="指定时间")


img_dir = Path(__file__).parent / "images"


def certificate(images, texts: List[str], args: Model):
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

    frame.draw_text(
        (1565, 1527),
        "{:04d}".format(time.year),
        allow_wrap=False,
        fontsize=60,
    )
    frame.draw_text(
        (1752, 1527),
        "{:02d}".format(time.month),
        allow_wrap=False,
        fontsize=60,
    )
    frame.draw_text(
        (1865, 1527),
        "{:02d}".format(time.day),
        allow_wrap=False,
        fontsize=60,
    )

    return frame.save_png()


add_meme(
    "certificate",
    certificate,
    min_texts=3,
    max_texts=3,
    default_texts=["小王", "优秀学生", "一年一班"],
    args_type=MemeArgsType(parser, Model),
    keywords=["奖状", "证书"],
)
