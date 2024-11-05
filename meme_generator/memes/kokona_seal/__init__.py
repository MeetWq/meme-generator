import random
from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage
from pydantic import Field

from meme_generator import (
    MemeArgsModel,
    MemeArgsType,
    ParserArg,
    ParserOption,
    add_meme,
)
from meme_generator.exception import MemeFeedback, TextOverLength
from meme_generator.tags import MemeTags

img_dir = Path(__file__).parent / "images"


help_text = "图片编号，范围为 1~12"


class Model(MemeArgsModel):
    number: int = Field(0, description=help_text)


args_type = MemeArgsType(
    args_model=Model,
    parser_options=[
        ParserOption(
            names=["-n", "--number"],
            args=[ParserArg(name="number", value="int")],
            help_text=help_text,
        ),
    ],
)


def kokona_seal(images, texts: list[str], args: Model):
    text = texts[0]
    if args.number == 0:
        num = random.randint(1, 9)
    elif 1 <= args.number <= 12:
        num = args.number
    else:
        raise MemeFeedback(f"图片编号错误，请选择 1~12")
    size = (288,155)
    points = ((0,70),(280,0),(320,150),(40,220))
    loc = (100,20)
    frame = BuildImage.open(img_dir / f"{num}.png")
    text_img = BuildImage.new("RGBA", size)
    padding = 0
    try:
        text_img.draw_text(
            (padding, padding, size[0] - padding, size[1] - padding),
            text,
            max_fontsize=150,
            min_fontsize=50,
            allow_wrap=False,
            lines_align="center",
            spacing=10,
            font_families=["FZShaoEr-M11S"],
            fill="#ff0000",
        )
    except ValueError:
        raise TextOverLength(text)
    frame.paste(text_img.perspective(points), loc, alpha=True)
    return frame.save_png()


add_meme(
    "kokona_seal",
    kokona_seal,
    min_texts=1,
    max_texts=1,
    default_texts=["满分"],
    args_type=args_type,
    keywords=["心奈印章"],
    tags=MemeTags.kokona,
    date_created=datetime(2024, 11, 5),
    date_modified=datetime(2024, 11, 5),
)
