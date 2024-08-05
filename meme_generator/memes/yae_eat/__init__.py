from pathlib import Path
from pil_utils import BuildImage
from meme_generator import add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif


img_dir = Path(__file__).parent / "images"


def yae_eat(images: list[BuildImage], texts, args):
    position_list = [
            (110,249),
            (119,228),
            (120,209),
            (119,202),
            (124,221)
        ]
    def maker(i: int) -> Maker:
        def make(img: BuildImage) -> BuildImage:
            yae= BuildImage.open(img_dir / f"{i:02d}.png")
            if i in list(range(4,9)):
                food = img.convert("RGBA").circle().resize((36,36), keep_ratio=True)
                if i == 8:
                    food = food.resize((36,27), keep_ratio=False)
                yae.paste(food, position_list[i-4], alpha=True)
            return yae

        return make

    return make_gif_or_combined_gif(
        images[0], maker, 16, 0.08, FrameAlignPolicy.extend_loop
    )


add_meme("yae_eat", yae_eat, min_images=1, max_images=1, keywords=["八重吃"])