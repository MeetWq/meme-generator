import random
from pathlib import Path
from typing import List

from pil_utils import BuildImage
from pydantic import Field

from meme_generator import MemeArgsModel, MemeArgsParser, MemeArgsType, add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


help = "图片编号，范围为 1~8"

parser = MemeArgsParser()
parser.add_argument("-n", "--number", type=int, default=0, help=help)


class Model(MemeArgsModel):
    number: int = Field(0, description=help)


def firefly_holdsign(images, texts: List[str], args: Model):
    text = texts[0]
    total_num = 8
    if 1 <= args.number <= total_num:
        num = args.number
    else:
        num = random.randint(1, total_num)

    params = [
        ((300, 200), (144, 322), ((0, 66), (276, 0), (319, 178), (43, 244))),
        ((300, 250), (-46, -50), ((0, 83), (312, 0), (348, 243), (46, 314))),
        ((300, 150), (106, 351), ((0, 0), (286, 0), (276, 149), (12, 149))),
        ((250, 200), (245, -6), ((31, 0), (288, 49), (256, 239), (0, 190))),
        ((500, 200), (0, 0), ((0, 0), (492, 0), (462, 198), (25, 198))),
        ((350, 150), (74, 359), ((0, 52), (345, 0), (364, 143), (31, 193))),
        ((270, 200), (231, -9), ((31, 0), (305, 49), (270, 245), (0, 192))),
        ((350, 150), (64, 340), ((0, 44), (345, 0), (358, 153), (34, 197))),
    ]
    size, loc, points = params[num - 1]
    frame = BuildImage.open(img_dir / f"{num:02d}.png")
    text_img = BuildImage.new("RGBA", size)
    padding = 10
    try:
        text_img.draw_text(
            (padding, padding, size[0] - padding, size[1] - padding),
            text,
            max_fontsize=80,
            min_fontsize=30,
            allow_wrap=True,
            lines_align="center",
            spacing=10,
            fontname="FZShaoEr-M11S",
            fill="#3b0b07",
        )
    except ValueError:
        raise TextOverLength(text)
    frame.paste(text_img.perspective(points), loc, alpha=True)
    return frame.save_png()


add_meme(
    "firefly_holdsign",
    firefly_holdsign,
    min_texts=1,
    max_texts=1,
    default_texts=["我超爱你"],
    args_type=MemeArgsType(parser, Model),
    keywords=["流萤举牌"],
)
