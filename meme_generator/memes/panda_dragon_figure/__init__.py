from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage
from pydantic import Field

from meme_generator import (
    CommandShortcut,
    MemeArgsModel,
    MemeArgsType,
    ParserArg,
    ParserOption,
    add_meme,
)
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"

help_text = "龙图名字"


class Model(MemeArgsModel):
    name: str = Field("", description=help_text)


args_type = MemeArgsType(
    args_model=Model,
    parser_options=[
        ParserOption(
            names=["-n", "--name"],
            args=[ParserArg(name="name", value="str")],
            help_text=help_text,
        ),
    ],
)


def panda_dragon_figure(images, texts: list[str], args: Model):
    name = args.name or "责怪龙"
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")

    try:
        frame.draw_text(
            (0, 470, 470, 550),
            name,
            allow_wrap=False,
            max_fontsize=60,
            min_fontsize=20,
            fill=(255, 255, 255),
        )
    except ValueError:
        raise TextOverLength(name)

    try:
        frame.draw_text(
            (0, 0, 550, 120),
            text,
            allow_wrap=True,
            lines_align="center",
            max_fontsize=100,
            min_fontsize=20,
            fill=(0, 0, 0),
        )
    except ValueError:
        raise TextOverLength(text)

    return frame.save_png()


add_meme(
    "panda_dragon_figure",
    panda_dragon_figure,
    min_texts=1,
    max_texts=1,
    default_texts=["我要玩原神"],
    args_type=args_type,
    keywords=["熊猫龙图"],
    shortcuts=[
        CommandShortcut(
            key=r"(?P<name>\S{1,10})龙[\s:：]+(?P<text>\S+)",
            args=["--name", "{name}龙", "{text}"],
            humanized="xx龙：xx",
        )
    ],
    date_created=datetime(2024, 10, 30),
    date_modified=datetime(2024, 10, 30),
)
