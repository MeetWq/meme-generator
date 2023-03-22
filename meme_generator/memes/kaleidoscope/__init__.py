import math
from typing import List

from pil_utils import BuildImage
from pydantic import Field

from meme_generator import MemeArgsModel, MemeArgsParser, MemeArgsType, add_meme
from meme_generator.utils import make_jpg_or_gif

help = "是否将图片变为圆形"

parser = MemeArgsParser(prefix_chars="-/")
parser.add_argument("--circle", "/圆", action="store_true", help=help)


class Model(MemeArgsModel):
    circle: bool = Field(False, description=help)


def kaleidoscope(images: List[BuildImage], texts, args: Model):
    def make(img: BuildImage) -> BuildImage:
        circle_num = 10
        img_per_circle = 4
        init_angle = 0
        angle_step = 360 / img_per_circle
        radius = lambda n: n * 50 + 100
        cx = cy = radius(circle_num)

        img = img.convert("RGBA")
        frame = BuildImage.new("RGBA", (cx * 2, cy * 2), "white")
        for i in range(circle_num):
            r = radius(i)
            img_w = i * 35 + 100
            im = img.resize_width(img_w)
            if args.circle:
                im = im.circle()
            for j in range(img_per_circle):
                angle = init_angle + angle_step * j
                im_rot = im.rotate(angle - 90, expand=True)
                x = round(cx + r * math.cos(math.radians(angle)) - im_rot.width / 2)
                y = round(cy - r * math.sin(math.radians(angle)) - im_rot.height / 2)
                frame.paste(im_rot, (x, y), alpha=True)
            init_angle += angle_step / 2
        return frame

    return make_jpg_or_gif(images[0], make)


add_meme(
    "kaleidoscope",
    kaleidoscope,
    min_images=1,
    max_images=1,
    args_type=MemeArgsType(parser, Model, [Model(circle=False), Model(circle=True)]),
    keywords=["万花筒", "万花镜"],
)
