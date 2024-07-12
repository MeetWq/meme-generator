from pydantic import Field

from PIL.Image import Transpose
from pil_utils import BuildImage

from meme_generator import MemeArgsModel, MemeArgsParser, MemeArgsType, add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

help = "是否将图片水平翻转"

parser = MemeArgsParser(prefix_chars="-/")
parser.add_argument("--horizontal", "/水平翻转", action="store_true", help=help)


class Model(MemeArgsModel):
    horizontal: bool = Field(False, description=help)


def patrol(images: list[BuildImage], texts, args: Model):
    # fmt: off
    locs = [
        (54, 16), (52, 13), (49, 10), (46, 9), (40, 10),
        (34, 13), (31, 16), (28, 13), (22, 10), (15, 10),
        (7, 12), (3, 14), (0, 16),
        (1, 16), (3, 13), (7, 10), (12, 10), (16, 9),
        (22, 11), (25, 13), (28, 16), (32, 12), (37, 9),
        (42, 7), (47, 7), (51, 9), (53, 11), (55, 14),
        (54, 16)
    ]
    # fmt: on
    def maker(i: int) -> Maker:
        def make(img: BuildImage) -> BuildImage:
            img = images[0].convert("RGBA").square()
            if args.horizontal:
                img = img.transpose(Transpose.FLIP_LEFT_RIGHT)
            if i >= 13:
                img = img.transpose(Transpose.FLIP_LEFT_RIGHT)
            frame = BuildImage.new("RGBA", (96, 57), "white")
            x, y = locs[i]
            frame.paste(img.resize_width(42), (x, y), alpha=True)
            return frame

        return make

    return make_gif_or_combined_gif(
        images[0], maker, 29, 0.05, FrameAlignPolicy.extend_loop
    )


add_meme(
    "patrol",
    patrol,
    min_images=1,
    max_images=1,
    args_type=MemeArgsType(
        parser, Model, [Model(horizontal=False), Model(horizontal=True)]
    ),
    keywords=["巡逻"],
)
