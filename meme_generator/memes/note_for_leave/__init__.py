from datetime import datetime

import dateparser
from pil_utils import BuildImage, Text2Image
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
    name: str = Field("", description="指定名字")


args_type = MemeArgsType(
    args_model=Model,
    parser_options=[
        ParserOption(
            names=["-t", "--time"],
            args=[ParserArg(name="time", value="str")],
            help_text="指定时间",
        ),
        ParserOption(
            names=["-n", "--name"],
            args=[ParserArg(name="name", value="str")],
            help_text="指定名字",
        ),
    ],
)

default_text = "想玩原神"


def note_for_leave(images: list[BuildImage], texts: list[str], args: Model):
    time = datetime.now()
    if args.time and (parsed_time := dateparser.parse(args.time)):
        time = parsed_time
    name = args.name or (args.user_infos[-1].name if args.user_infos else "")
    text = texts[0] if texts else default_text
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
    try:
        frame.draw_text(
            (40, 300, 285, 700),
            text=text,
            max_fontsize=90,
            min_fontsize=40,
            allow_wrap=True,
            lines_align="center",
            fill="red",
        )
    except ValueError:
        raise TextOverLength(text)
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
    default_texts=[default_text],
    args_type=args_type,
    keywords=["请假条"],
    date_created=datetime(2023, 4, 27),
    date_modified=datetime(2023, 4, 27),
)
