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
from meme_generator.exception import MemeFeedback

img_dir = Path(__file__).parent / "images"


help_text = "图片编号，范围为 1~92"


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


def crawl(images: list[BuildImage], texts: list[str], args: Model):
    total_num = 92
    if args.number == 0:
        num = random.randint(1, total_num)
    elif 1 <= args.number <= total_num:
        num = args.number
    else:
        raise MemeFeedback(f"图片编号错误，请选择 1~{total_num}")

    img = images[0].convert("RGBA").circle().resize((100, 100))
    frame = BuildImage.open(img_dir / f"{num:02d}.jpg")
    frame.paste(img, (0, 400), alpha=True)
    return frame.save_jpg()


add_meme(
    "crawl",
    crawl,
    min_images=1,
    max_images=1,
    args_type=args_type,
    keywords=["爬"],
    date_created=datetime(2021, 5, 5),
    date_modified=datetime(2023, 2, 14),
)
