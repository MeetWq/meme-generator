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

    paddings = (55, 43, 50, 36, 40, 33, 36, 38, 33, 46, 26, 33)
    frame = BuildImage.open(img_dir / f"{num:02d}.png")
    padding = paddings[num - 1]

    try:
        frame.draw_text(
            (0, frame.height - padding, frame.width, frame.height),
            text,
            max_fontsize=50,
            min_fontsize=20,
            allow_wrap=True,
            lines_align="center",
            font_families=["FZShaoEr-M11S"],
            fill="black",
        )
    except ValueError:
        raise TextOverLength(text)
    return frame.save_png()


add_meme(
    "jinhsi",
    jinhsi,
    min_texts=1,
    max_texts=1,
    default_texts=["汐汐"],
    args_type=args_type,
    keywords=["汐汐", "今汐"],
    tags=MemeTags.jinhsi,
    date_created=datetime(2024, 12, 7),
    date_modified=datetime(2024, 12, 7),
)
