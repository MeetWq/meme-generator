from typing import Dict, List, Literal, NamedTuple, Tuple

from PIL.Image import Transpose
from pil_utils import BuildImage
from pydantic import Field

from meme_generator import MemeArgsModel, MemeArgsParser, MemeArgsType, add_meme
from meme_generator.utils import make_jpg_or_gif

help = "对称方向"

parser = MemeArgsParser(prefix_chars="-/")
group = parser.add_mutually_exclusive_group()
group.add_argument(
    "-d",
    "--direction",
    type=str,
    choices=["left", "right", "top", "bottom"],
    default="left",
    help=help,
)
group.add_argument("--left", "/左", action="store_const", const="left", dest="direction")
group.add_argument(
    "--right", "/右", action="store_const", const="right", dest="direction"
)
group.add_argument("--top", "/上", action="store_const", const="top", dest="direction")
group.add_argument(
    "--bottom", "/下", action="store_const", const="bottom", dest="direction"
)


class Model(MemeArgsModel):
    direction: Literal["left", "right", "top", "bottom"] = Field(
        "left", description=help
    )


def symmetric(images: List[BuildImage], texts, args: Model):
    img = images[0]
    img_w, img_h = img.size

    class Mode(NamedTuple):
        method: Transpose
        frame_size: Tuple[int, int]
        size1: Tuple[int, int, int, int]
        pos1: Tuple[int, int]
        size2: Tuple[int, int, int, int]
        pos2: Tuple[int, int]

    modes: Dict[str, Mode] = {
        "left": Mode(
            Transpose.FLIP_LEFT_RIGHT,
            (img_w // 2 * 2, img_h),
            (0, 0, img_w // 2, img_h),
            (0, 0),
            (img_w // 2, 0, img_w // 2 * 2, img_h),
            (img_w // 2, 0),
        ),
        "right": Mode(
            Transpose.FLIP_LEFT_RIGHT,
            (img_w // 2 * 2, img_h),
            (img_w // 2, 0, img_w // 2 * 2, img_h),
            (img_w // 2, 0),
            (0, 0, img_w // 2, img_h),
            (0, 0),
        ),
        "top": Mode(
            Transpose.FLIP_TOP_BOTTOM,
            (img_w, img_h // 2 * 2),
            (0, 0, img_w, img_h // 2),
            (0, 0),
            (0, img_h // 2, img_w, img_h // 2 * 2),
            (0, img_h // 2),
        ),
        "bottom": Mode(
            Transpose.FLIP_TOP_BOTTOM,
            (img_w, img_h // 2 * 2),
            (0, img_h // 2, img_w, img_h // 2 * 2),
            (0, img_h // 2),
            (0, 0, img_w, img_h // 2),
            (0, 0),
        ),
    }

    mode = modes[args.direction]

    def make(img: BuildImage) -> BuildImage:
        first = img.convert("RGBA")
        second = img.convert("RGBA").transpose(mode.method)
        frame = BuildImage.new("RGBA", mode.frame_size)
        frame.paste(first.crop(mode.size1), mode.pos1, alpha=True)
        frame.paste(second.crop(mode.size2), mode.pos2, alpha=True)
        return frame

    return make_jpg_or_gif(img, make, keep_transparency=True)


add_meme(
    "symmetric",
    symmetric,
    min_images=1,
    max_images=1,
    args_type=MemeArgsType(
        parser,
        Model,
        [
            Model(direction="left"),
            Model(direction="right"),
            Model(direction="top"),
            Model(direction="bottom"),
        ],
    ),
    keywords=["对称"],
)
