from typing import List

from pil_utils import BuildImage
from pydantic import Field

from meme_generator import MemeArgsModel, MemeArgsParser, MemeArgsType, add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif

help = "图片“压扁”比例"

parser = MemeArgsParser()
parser.add_argument("-r", "--ratio", type=int, default=2, help=help)


class Model(MemeArgsModel):
    ratio: int = Field(2, description=help)


def look_flat(images: List[BuildImage], texts: List[str], args: Model):
    text = texts[0] if texts else "可恶...被人看扁了"
    ratio = args.ratio

    img_w = 500
    text_h = 80
    text_frame = BuildImage.new("RGBA", (img_w, text_h), "white")
    try:
        text_frame.draw_text(
            (10, 0, img_w - 10, text_h),
            text,
            max_fontsize=55,
            min_fontsize=30,
            weight="bold",
        )
    except ValueError:
        raise TextOverLength(text)

    def make(img: BuildImage) -> BuildImage:
        img = img.convert("RGBA").resize_width(img_w)
        img = img.resize((img_w, img.height // ratio))
        img_h = img.height
        frame = BuildImage.new("RGBA", (img_w, img_h + text_h), "white")
        return frame.paste(img, alpha=True).paste(text_frame, (0, img_h), alpha=True)

    return make_jpg_or_gif(images[0], make)


add_meme(
    "look_flat",
    look_flat,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=["可恶...被人看扁了"],
    args_type=MemeArgsType(parser, Model),
    keywords=["看扁"],
)
