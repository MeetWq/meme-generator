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
from meme_generator.exception import MemeFeedback, TextOverLength
from meme_generator.utils import make_jpg_or_gif

help_text = "图片“压扁”比例，默认为 2"


class Model(MemeArgsModel):
    ratio: int = Field(2, description=help_text)


args_type = MemeArgsType(
    args_model=Model,
    parser_options=[
        ParserOption(
            names=["-r", "--ratio"],
            args=[ParserArg(name="ratio", value="int")],
            help_text=help_text,
        ),
    ],
)

default_text = "可恶...被人看扁了"


def look_flat(images: list[BuildImage], texts: list[str], args: Model):
    text = texts[0] if texts else default_text
    ratio = args.ratio
    if not 1 <= ratio < images[0].height:
        raise MemeFeedback("请输入合适的“压扁”比例")

    img_w = 500
    text_h = 80
    text_frame = BuildImage.new("RGBA", (img_w, text_h), "white")
    try:
        text_frame.draw_text(
            (10, 0, img_w - 10, text_h),
            text,
            max_fontsize=55,
            min_fontsize=30,
            font_style="bold",
        )
    except ValueError:
        raise TextOverLength(text)

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize_width(img_w)
        img = img.resize((img_w, img.height // ratio))
        img_h = img.height
        frame = BuildImage.new("RGBA", (img_w, img_h + text_h), "white")
        return frame.paste(img, alpha=True).paste(text_frame, (0, img_h), alpha=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "look_flat",
    look_flat,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=[default_text],
    args_type=args_type,
    keywords=["看扁"],
    date_created=datetime(2022, 10, 6),
    date_modified=datetime(2023, 2, 14),
)
