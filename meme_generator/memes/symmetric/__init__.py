from PIL import Image
from pil_utils import BuildImage
from collections import namedtuple
from argparse import ArgumentParser
from typing import List, Dict, Literal

from meme_generator.utils import make_jpg_or_gif
from meme_generator import add_meme, MemeArgsType, MemeArgsModel


parser = ArgumentParser(prefix_chars="-/")
parser.add_argument(
    "--left", "/左", action="store_const", const="left", dest="direction"
)
parser.add_argument(
    "--right", "/右", action="store_const", const="right", dest="direction"
)
parser.add_argument("--top", "/上", action="store_const", const="top", dest="direction")
parser.add_argument(
    "--bottom", "/下", action="store_const", const="bottom", dest="direction"
)
parser.add_argument(
    "-d",
    "--direction",
    type=str,
    choices=["left", "right", "top", "bottom"],
    default="left",
)


class Model(MemeArgsModel):
    direction: Literal["left", "right", "top", "bottom"] = "left"


def symmetric(images: List[BuildImage], texts, args: Model):
    img = images[0]
    img_w, img_h = img.size

    Mode = namedtuple(
        "Mode", ["method", "frame_size", "size1", "pos1", "size2", "pos2"]
    )
    modes: Dict[str, Mode] = {
        "left": Mode(
            Image.FLIP_LEFT_RIGHT,
            (img_w // 2 * 2, img_h),
            (0, 0, img_w // 2, img_h),
            (0, 0),
            (img_w // 2, 0, img_w // 2 * 2, img_h),
            (img_w // 2, 0),
        ),
        "right": Mode(
            Image.FLIP_LEFT_RIGHT,
            (img_w // 2 * 2, img_h),
            (img_w // 2, 0, img_w // 2 * 2, img_h),
            (img_w // 2, 0),
            (0, 0, img_w // 2, img_h),
            (0, 0),
        ),
        "top": Mode(
            Image.FLIP_TOP_BOTTOM,
            (img_w, img_h // 2 * 2),
            (0, 0, img_w, img_h // 2),
            (0, 0),
            (0, img_h // 2, img_w, img_h // 2 * 2),
            (0, img_h // 2),
        ),
        "bottom": Mode(
            Image.FLIP_TOP_BOTTOM,
            (img_w, img_h // 2 * 2),
            (0, img_h // 2, img_w, img_h // 2 * 2),
            (0, img_h // 2),
            (0, 0, img_w, img_h // 2),
            (0, 0),
        ),
    }

    mode = modes[args.direction]

    def make(img: BuildImage) -> BuildImage:
        first = img
        second = img.transpose(mode.method)
        frame = BuildImage.new("RGBA", mode.frame_size)
        frame.paste(first.crop(mode.size1), mode.pos1)
        frame.paste(second.crop(mode.size2), mode.pos2)
        return frame

    return make_jpg_or_gif(img, make, keep_transparency=True)


add_meme(
    "symmetric",
    symmetric,
    min_images=1,
    max_images=1,
    args_type=MemeArgsType(parser, Model),
    keywords=["对称"],
)
