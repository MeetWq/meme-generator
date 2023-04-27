import datetime
import re
from typing import List

from pil_utils import BuildImage
from pydantic import Field

from meme_generator import MemeArgsModel, MemeArgsParser, MemeArgsType, add_meme
from meme_generator.exception import TextOverLength

help = "指定时间"

parser = MemeArgsParser()
parser.add_argument(
    "-t",
    "--time",
    type=str,
    default="",
    help=help,
)


class Model(MemeArgsModel):
    time: str = Field("", description=help)


def note_for_leave(images: List[BuildImage], texts: List[str], args: Model):
    time_re = r"\d{4}\.\d{1,2}\.\d{1,2}"
    time = (
        datetime.datetime.now().strftime("%Y.%m.%d")
        if args.time == "" or not re.match(time_re, args.time)
        else args.time
    )
    time_ls = time.split(".")
    name = (texts[0] if texts else "") or (
        args.user_infos[-1].name if args.user_infos else ""
    )
    img = (
        images[0]
        .convert("RGBA")
        .resize((410, 400), keep_ratio=True, inside=True, bg_color="white")
    )
    frame = BuildImage.new("RGBA", (830, 1024), "white")
    frame.draw_text(
        (270, 78, 589, 180),
        text="请假条",
        max_fontsize=90,
        min_fontsize=50,
    )
    try:
        frame.draw_text(
            (113, 249, 466, 310),
            text="本人" + name + "因",
            max_fontsize=50,
            min_fontsize=21,
            allow_wrap=True,
        )
    except TextOverLength:
        raise TextOverLength(name)
    frame.draw_text(
        (124, 431, 335, 531),
        text="想玩",
        max_fontsize=90,
        min_fontsize=70,
        fill="red",
    )
    frame.paste(img, (338, 311))
    frame.draw_text(
        (90, 709, 780, 770),
        text=f"于{time_ls[0]}年{time_ls[1]}月{time_ls[2]}日请假一天,",
        max_fontsize=50,
        min_fontsize=30,
        halign="left",
    )
    frame.draw_text(
        (90, 793, 780, 875),
        text="望领导批准！！！",
        max_fontsize=75,
        min_fontsize=40,
        halign="left",
    )
    return frame.save_jpg()


add_meme(
    "note_for_leave",
    note_for_leave,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    args_type=MemeArgsType(parser, Model, [Model(time="1145.1.4")]),
    keywords=["请假条"],
)
