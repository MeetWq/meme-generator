import math
from datetime import datetime

from arclet.alconna import store_true
from pil_utils import BuildImage
from pydantic import Field

from meme_generator import MemeArgsModel, MemeArgsType, ParserOption, add_meme
from meme_generator.utils import make_jpg_or_gif

help_text = "是否将图片变为圆形"


class Model(MemeArgsModel):
    circle: bool = Field(False, description=help_text)


args_type = MemeArgsType(
    args_model=Model,
    args_examples=[Model(circle=False), Model(circle=True)],
    parser_options=[
        ParserOption(
            names=["--circle", "圆"],
            default=False,
            action=store_true,
            help_text=help_text,
        ),
    ],
)


def kaleidoscope(images: list[BuildImage], texts, args: Model):
    def make(imgs: list[BuildImage]) -> BuildImage:
        circle_num = 10
        img_per_circle = 4
        init_angle = 0
        angle_step = 360 / img_per_circle

        def radius(n):
            return n * 50 + 100

        cx = cy = radius(circle_num)

        img = imgs[0].convert("RGBA")
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

    return make_jpg_or_gif(images, make)


add_meme(
    "kaleidoscope",
    kaleidoscope,
    min_images=1,
    max_images=1,
    args_type=args_type,
    keywords=["万花筒", "万花镜"],
    date_created=datetime(2023, 1, 8),
    date_modified=datetime(2023, 2, 14),
)
