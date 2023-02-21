from typing import List
from pil_utils import BuildImage
from argparse import ArgumentParser

from meme_generator.utils import make_jpg_or_gif
from meme_generator.exception import TextOverLength
from meme_generator import add_meme, MemeArgsType, MemeArgsModel


parser = ArgumentParser()
parser.add_argument("-r", "--ratio", type=int, default=2)


class Model(MemeArgsModel):
    ratio: int = 2


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
        img = images[0].convert("RGBA").resize_width(img_w)
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
