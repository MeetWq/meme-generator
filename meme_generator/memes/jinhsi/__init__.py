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


def jinhsi(images, texts: list[str], args: Model):
    text = texts[0]
    total_num = 12
    if args.number == 0:
        num = random.randint(1, total_num)
    elif 1 <= args.number <= total_num:
        num = args.number
    else:
        raise MemeFeedback(f"图片编号错误，请选择 1~{total_num}")

    params = [
        ((320, 375), (39, 155), ((0, 0), (140, 0), (140, 148), (0, 148))),
        ((320, 375), (39, 160), ((0, 0), (140, 0), (140, 148), (0, 148))),
        ((320, 375), (39, 160), ((0, 0), (140, 0), (140, 148), (0, 148))),
        ((320, 375), (39, 165), ((0, 0), (140, 0), (140, 148), (0, 148))),
        ((320, 375), (39, 162), ((0, 0), (140, 0), (140, 148), (0, 148))),
        ((320, 375), (39, 166), ((0, 0), (140, 0), (140, 148), (0, 148))),
        ((320, 375), (39, 164), ((0, 0), (140, 0), (140, 148), (0, 148))),
        ((320, 375), (39, 164), ((0, 0), (140, 0), (140, 148), (0, 148))),
        ((320, 375), (39, 165), ((0, 0), (140, 0), (140, 148), (0, 148))),
        ((320, 375), (39, 160), ((0, 0), (140, 0), (140, 148), (0, 148))),
        ((320, 375), (39, 169), ((0, 0), (140, 0), (140, 148), (0, 148))),
        ((320, 375), (39, 166), ((0, 0), (140, 0), (140, 148), (0, 148))),
        ]
    size, loc, points = params[num - 1]
    frame = BuildImage.open(img_dir / f"{num:02d}.png")
    text_img = BuildImage.new("RGBA", size)
    padding = 0
    try:
        text_img.draw_text(
            (padding, padding, size[0] - padding, size[1] - padding),
            text,
            max_fontsize=40,
            min_fontsize=40,
            allow_wrap=True,
            lines_align="center",
            font_families=["FZShaoEr-M11S"],
            fill="#3b0b07",
        )
    except ValueError:
        raise TextOverLength(text)
    frame.paste(text_img.perspective(points), loc, alpha=True)
    return frame.save_png()


add_meme(
    "jinhsi",
    jinhsi,
    min_texts=1,
    max_texts=8,
    default_texts=["汐汐"],
    args_type=args_type,
    keywords=["汐汐","今汐"],
    tags=MemeTags.jinhsi,
    date_created=datetime(2024, 5, 5),
    date_modified=datetime(2024, 5, 6),
)

