from pathlib import Path
from pil_utils import BuildImage
from pydantic import Field
from meme_generator import MemeArgsModel, MemeArgsParser, MemeArgsType,add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif


img_dir = Path(__file__).parent / "images"

parser = MemeArgsParser(prefix_chars="-/")
parser.add_argument("--character", "/角色", help="角色1--八重神子，2--胡桃，3--妮露，4--可莉，5--刻晴，6--钟离")

class Model(MemeArgsModel):
    character: int = Field(1,description="角色1--八重神子，2--胡桃，3--妮露，4--可莉，5--刻晴，6--钟离")

def genshin_eat(images: list[BuildImage], texts, args:Model):
    if args.character not in range(1,7):
        raise ValueError("角色参数错误，请选择1-6")
    position_list = [
            (110,249),
            (119,228),
            (120,209),
            (119,202),
            (124,221)
        ]
    def maker(i: int) -> Maker:
        def make(img: BuildImage) -> BuildImage:
            chara= BuildImage.open(img_dir / f"{args.character}_{i:02d}.png")
            if i in list(range(4,9)):
                food = img.convert("RGBA").circle().resize((36,36), keep_ratio=True)
                if i == 8:
                    food = food.resize((36,27), keep_ratio=False)
                chara.paste(food, position_list[i-4], alpha=True)
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
    args_type=MemeArgsType(parser, Model, [Model(character=i) for i in range(1,7)]),
    keywords=["原神吃"])