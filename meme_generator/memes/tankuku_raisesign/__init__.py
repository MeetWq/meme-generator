from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def tankuku_raisesign(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").resize((300, 230), keep_ratio=True)
    params = (
        (((0, 46), (320, 0), (350, 214), (38, 260)), (68, 91)),
        (((18, 0), (328, 28), (298, 227), (0, 197)), (184, 77)),
        (((15, 0), (294, 28), (278, 216), (0, 188)), (194, 65)),
        (((14, 0), (279, 27), (262, 205), (0, 178)), (203, 55)),
        (((14, 0), (270, 25), (252, 195), (0, 170)), (209, 49)),
        (((15, 0), (260, 25), (242, 186), (0, 164)), (215, 41)),
        (((10, 0), (245, 21), (230, 180), (0, 157)), (223, 35)),
        (((13, 0), (230, 21), (218, 168), (0, 147)), (231, 25)),
        (((13, 0), (220, 23), (210, 167), (0, 140)), (238, 21)),
        (((27, 0), (226, 46), (196, 182), (0, 135)), (254, 13)),
        (((27, 0), (226, 46), (196, 182), (0, 135)), (254, 13)),
        (((27, 0), (226, 46), (196, 182), (0, 135)), (254, 13)),
        (((0, 35), (200, 0), (224, 133), (25, 169)), (175, 9)),
        (((0, 35), (200, 0), (224, 133), (25, 169)), (195, 17)),
        (((0, 35), (200, 0), (224, 133), (25, 169)), (195, 17)),
    )
    frames: List[IMG] = []
    for i in range(15):
        points, pos = params[i]
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(img.perspective(points), pos, below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.2)


add_meme(
    "tankuku_raisesign",
    tankuku_raisesign,
    min_images=1,
    max_images=1,
    keywords=["唐可可举牌"],
)
