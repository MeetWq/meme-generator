from pydantic import Field

from pil_utils import BuildImage

from meme_generator import MemeArgsModel, MemeArgsParser, MemeArgsType, add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

help = "是否改为水平循环"

parser = MemeArgsParser(prefix_chars="-/")
parser.add_argument("--horizontal", "/水平", action="store_true", help=help)


class Model(MemeArgsModel):
    horizontal: bool = Field(False, description=help)


def loop(images: list[BuildImage], texts, args: Model):
    def maker(i: int) -> Maker:
        def make(img: BuildImage) -> BuildImage:
            img = img.convert("RGBA")
            width, height = img.size
            if not args.horizontal:
                extend_img = BuildImage.new("RGBA", (width, height * 2), "white")
                extend_img.paste(img, (0, 0))
                extend_img.paste(img, (0, height))
                return extend_img.crop(
                    (0, int(height / 30 * i), width, int(height / 30 * i) + height)
                )
            extend_img = BuildImage.new("RGBA", (width * 2, height), "white")
            extend_img.paste(img, (0, 0))
            extend_img.paste(img, (width, 0))
            return extend_img.crop(
                (int(width / 30 * i), 0, int(width / 30 * i) + width, height)
            )

        return make

    return make_gif_or_combined_gif(
        images[0], maker, 30, 0.05, FrameAlignPolicy.extend_loop
    )


add_meme(
    "loop",
    loop,
    min_images=1,
    max_images=1,
    args_type=MemeArgsType(
        parser, Model, [Model(horizontal=False), Model(horizontal=True)]
    ),
    keywords=["循环"],
)
