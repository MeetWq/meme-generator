from datetime import datetime

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
from meme_generator.utils import make_jpg_or_gif

help_text = "像素化大小，默认为 10"


class Model(MemeArgsModel):
    number: int = Field(10, description=help_text)


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


def pixelate(images: list[BuildImage], texts, args: Model):
    num = args.number
    if not (1 <= num < min(images[0].size)):
        raise MemeFeedback("请输入合适的像素化大小")

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0]
        image = img.image
        image = image.resize((img.width // num, img.height // num), resample=0)
        image = image.resize(img.size, resample=0)
        return BuildImage(image)

    return make_jpg_or_gif(images, make)


add_meme(
    "pixelate",
    pixelate,
    min_images=1,
    max_images=1,
    keywords=["像素化"],
    args_type=args_type,
    date_created=datetime(2024, 8, 12),
    date_modified=datetime(2024, 8, 12),
)
