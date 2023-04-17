from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def capoo_rip(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").resize((150, 100), inside=True, bg_color="white")
    img_L = img.crop((0, 0, 75, 100))
    img_R = img.crop((75, 0, 150, 100))
    params = [
        [
            [(89, 156), 2.9, ((0, 0), (80, 0), (94, 100), (14, 100))],
            [(192, 151), 4, ((0, 7), (79, 3), (82, 107), (11, 112))],
        ],
        [[(61, 196), 0, ((140, 68), (0, 59), (33, 0), (165, 8))]],
        [[(63, 196), 0, ((136, 68), (0, 59), (29, 0), (158, 13))]],
        [
            [(62, 195), 0, ((137, 72), (0, 58), (27, 0), (167, 11))],
        ],
        [
            [(62, 199), 0, ((139, 66), (0, 56), (30, 0), (161, 11))],
        ],
        [
            [(62, 197), 0, ((137, 70), (0, 56), (30, 0), (162, 8))],
        ],
        [
            [(63, 196), 0, ((134, 72), (0, 57), (27, 0), (162, 13))],
        ],
        [
            [(62, 200), 0, ((139, 64), (0, 53), (28, 0), (159, 16))],
        ],
        [
            [(62, 199), 0, ((136, 66), (0, 53), (28, 0), (161, 17))],
        ],
        [
            [(62, 196), 0, ((138, 71), (0, 56), (30, 0), (161, 11))],
        ],
        [
            [(95, 152), 0, ((0, 8), (155, 0), (163, 107), (13, 112))],
        ],
        [
            [(108, 129), 0, ((0, 6), (128, 0), (136, 113), (10, 117))],
        ],
        [
            [(84, 160), 0, ((0, 6), (184, 0), (190, 90), (10, 97))],
        ],
        [
            [(78, 158), 0, ((0, 3), (86, 0), (97, 106), (16, 106))],
            [(195, 156), 0, ((0, 4), (82, 0), (85, 106), (15, 110))],
        ],
        [
            [(89, 156), 2.9, ((0, 0), (80, 0), (94, 100), (14, 100))],
            [(192, 151), 4, ((0, 7), (79, 3), (82, 107), (11, 112))],
        ],
    ]

    frames: List[IMG] = []

    for i in range(15):
        raw_frames = BuildImage.open(img_dir / f"{i}.png")
        if i in [0, 13, 14]:
            raw_frames.paste(
                img_R.perspective(params[i][1][2]), params[i][1][0], below=True
            )
            raw_frames.paste(
                img_L.perspective(params[i][0][2]), params[i][0][0], below=True
            )
            frames.append(raw_frames.image)
        else:
            raw_frames.paste(
                img.perspective(params[i][0][2]), params[i][0][0], below=True
            )
            frames.append(raw_frames.image)

    return save_gif(frames, 0.1)


add_meme(
    "capoo_rip",
    capoo_rip,
    min_images=1,
    max_images=1,
    keywords=["咖波撕"],
)
