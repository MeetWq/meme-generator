from datetime import datetime
from typing import List

import dateparser
from pil_utils import BuildImage, Text2Image
from pydantic import Field

from meme_generator import MemeArgsModel, MemeArgsParser, MemeArgsType, add_meme
from meme_generator.exception import TextOverLength

help = "指定时间"

parser = MemeArgsParser()
parser.add_argument("--time", type=str, default="", help=help)


class Model(MemeArgsModel):
    time: str = Field("", description=help)


def note_for_leave(images: List[BuildImage], texts: List[str], args: Model):
    time = datetime.now()
    if args.time and (parsed_time := dateparser.parse(args.time)):
        time = parsed_time
    name = texts[0] if texts else (args.user_infos[-1].name if args.user_infos else "")
    img = (
        images[0]
        .convert("RGBA")
        .resize((450, 400), keep_ratio=True, inside=True, bg_color="white")
    )

    frame = BuildImage.new("RGBA", (800, 950), "white")
    frame.draw_text(
        (40, 20, 760, 180),
        text="请假条",
        weight="bold",
        max_fontsize=100,
        min_fontsize=80,
    )
    frame.draw_text((40, 200), "本人", fontsize=50)
    name_width = Text2Image.from_text(name, fontsize=50).width
    if (name_width) > 800:
        raise TextOverLength(name)
    name_width = min(450, max(150, name_width)) + 50
    frame.draw_text(
        (150, 200, 150 + name_width, 265), text=name, max_fontsize=50, min_fontsize=20
    )
    frame.draw_line((150, 260, 150 + name_width, 260), fill="black", width=4)
    frame.draw_text((160 + name_width, 200), "因", fontsize=50)
    frame.draw_text((70, 390), text="想玩", fontsize=90, fill="red")
    frame.paste(img, (300, 290))
    frame.draw_bbcode_text(
        (40, 700, 760, 800),
        text=f"于[u] {time.year} [/u]年[u] {time.month} [/u]月[u] {time.day} [/u]日请假一天,",
        max_fontsize=50,
        min_fontsize=30,
        halign="left",
    )
    frame.draw_text((40, 800), text="望领导批准！！！", fontsize=75, weight="bold")
    return frame.save_jpg()


add_meme(
    "note_for_leave",
    note_for_leave,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    args_type=MemeArgsType(parser, Model),
    keywords=["请假条"],
)
