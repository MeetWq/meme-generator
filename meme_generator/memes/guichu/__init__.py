from typing import Dict, List, Literal, NamedTuple, Tuple

from PIL.Image import Image as IMG
from PIL.Image import Transpose
from pil_utils import BuildImage
from pydantic import Field

from meme_generator import MemeArgsModel, MemeArgsParser, MemeArgsType, add_meme
from meme_generator.utils import save_gif

help = "鬼畜对称方向"

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


def guichu(images: List[BuildImage], texts, args: Model):
    img = images[0].convert("RGBA")
    img_w, img_h = img.size

    class Mode(NamedTuple):
        method: Transpose
        size1: Tuple[int, int, int, int]
        pos1: Tuple[int, int]
        size2: Tuple[int, int, int, int]
        pos2: Tuple[int, int]

    modes: Dict[str, Mode] = {
        "left": Mode(
            Transpose.FLIP_LEFT_RIGHT,
            (0, 0, img_w // 2, img_h),
            (0, 0),
            (img_w // 2, 0, img_w // 2 * 2, img_h),
            (img_w // 2, 0),
        ),
        "right": Mode(
            Transpose.FLIP_LEFT_RIGHT,
            (img_w // 2, 0, img_w // 2 * 2, img_h),
            (img_w // 2, 0),
            (0, 0, img_w // 2, img_h),
            (0, 0),
        ),
        "top": Mode(
            Transpose.FLIP_TOP_BOTTOM,
            (0, 0, img_w, img_h // 2),
            (0, 0),
            (0, img_h // 2, img_w, img_h // 2 * 2),
            (0, img_h // 2),
        ),
        "bottom": Mode(
            Transpose.FLIP_TOP_BOTTOM,
            (0, img_h // 2, img_w, img_h // 2 * 2),
            (0, img_h // 2),
            (0, 0, img_w, img_h // 2),
            (0, 0),
        ),
    }
    mode = modes[args.direction]

    img_flip = img.transpose(mode.method)
    img_symmetric = BuildImage.new("RGBA", img.size)
    img_symmetric.paste(img.crop(mode.size1), mode.pos1, alpha=True)
    img_symmetric.paste(img_flip.crop(mode.size2), mode.pos2, alpha=True)
    img_symmetric_big = BuildImage.new("RGBA", img.size)
    img_symmetric_big.paste(
        img_symmetric.copy().resize_width(img_w * 2), (-img_w // 2, -img_h // 2)
    )

    frames: List[IMG] = []
    frames += (
        ([img.image] * 3 + [img_flip.image] * 3) * 3
        + [img.image, img_flip.image] * 3
        + ([img_symmetric.image] * 2 + [img_symmetric_big.image] * 2) * 2
    )

    return save_gif(frames, 0.20)


add_meme(
    "guichu",
    guichu,
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
    keywords=["鬼畜"],
)
