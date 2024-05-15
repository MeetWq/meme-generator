from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def blood_pressure(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    def make(img: BuildImage) -> BuildImage:
        img = img.convert("RGBA").resize((414, 450), keep_ratio=True)
        return frame.copy().paste(img, (16, 17), below=True)

    return make_jpg_or_gif(images[0], make)


add_meme(
    "blood_pressure", blood_pressure, min_images=1, max_images=1, keywords=["高血压"]
)
