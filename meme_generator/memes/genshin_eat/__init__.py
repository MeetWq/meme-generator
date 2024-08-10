from pathlib import Path

from pil_utils import BuildImage
from pydantic import Field

from meme_generator import MemeArgsModel, MemeArgsParser, MemeArgsType, add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

img_dir = Path(__file__).parent / "images"

help_text = "角色：1、八重神子，2、胡桃，3、妮露，4、可莉，5、刻晴，6、钟离"

parser = MemeArgsParser(prefix_chars="-/")
parser.add_argument("--character", "/角色", help=help_text, default=1)


class Model(MemeArgsModel):
    character: int = Field(1, description=help_text)


def genshin_eat(images: list[BuildImage], texts, args: Model):
    if args.character not in range(1, 7):
        raise ValueError("角色参数错误，请选择1-6")
    name = ["yae_miko", "hutao", "nilou", "klee", "keqing", "zhongli"][
        args.character - 1
    ]

    position_list = [(106,245),(115,224),(116,205),(115,198),(120,217)]

    def maker(i: int) -> Maker:
        def make(img: BuildImage) -> BuildImage:
            chara = BuildImage.open(img_dir / name / f"{i:02d}.png")
            if i in range(4, 9):
                food = img.convert("RGBA").circle().resize((44, 44), keep_ratio=True)
                if i == 8:
                    food = food.resize((44, 33))
                chara.paste(food, position_list[i - 4], alpha=True)
            return chara

        return make

    return make_gif_or_combined_gif(
        images[0], maker, 16, 0.08, FrameAlignPolicy.extend_loop
    )


add_meme(
    "genshin_eat",
    genshin_eat,
    min_images=1,
    max_images=1,
    args_type=MemeArgsType(parser, Model, [Model(character=i) for i in range(1, 7)]),
    keywords=["原神吃"],
    # TODO: patterns=
)
