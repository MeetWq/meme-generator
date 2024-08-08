from pathlib import Path
from pil_utils import BuildImage
from meme_generator import add_meme
from meme_generator.utils import make_png_or_gif


img_dir = Path(__file__).parent / "images"


def jerry_stare(images: list[BuildImage], texts, args):
    jerry = BuildImage.open(img_dir / "0.png").convert("RGBA")

    def make(img: BuildImage) -> BuildImage:
        img = img.convert("RGBA").circle().resize((150, 150), keep_ratio=True)
        return jerry.copy().paste(img, (184, 268), img, below=True)

    return make_png_or_gif(images[0], make)


add_meme("jerry_stare", jerry_stare, min_images=1, max_images=1, keywords=["杰瑞盯"])
