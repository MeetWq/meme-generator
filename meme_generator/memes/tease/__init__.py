from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def tease(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").square()
    frames: list[IMG] = []
    params = [
        ((21, 75), ((0, 0), (129, 3), (155, 123), (12, 142))),
        ((18, 73), ((0, 29), (128, 0), (149, 118), (30, 147))),
        ((22, 78), ((0, 37), (136, 1), (160, 97), (16, 152))),
        ((22, 58), ((0, 58), (169, 1), (194, 92), (24, 170))),
        ((43, 23), ((0, 114), (166, 1), (168, 98), (41, 205))),
        ((38, 24), ((0, 112), (171, 0), (169, 113), (45, 195))),
        ((31, 54), ((0, 73), (148, 0), (172, 81), (45, 170))),
        ((24, 62), ((0, 62), (159, 1), (177, 81), (47, 155))),
        ((31, 75), ((1, 45), (126, 1), (158, 81), (29, 145))),
        ((18, 61), ((0, 63), (161, 1), (190, 88), (42, 153))),
        ((20, 66), ((0, 57), (152, 0), (195, 82), (40, 149))),
        ((16, 77), ((0, 41), (141, 0), (170, 90), (27, 138))),
        ((28, 105), ((0, 1), (132, 0), (131, 112), (1, 114))),
        ((21, 107), ((0, 1), (132, 0), (131, 112), (1, 114))),
        ((11, 113), ((1, 7), (138, 0), (141, 126), (4, 131))),
        ((10, 114), ((0, 0), (142, 0), (142, 131), (0, 131))),
        ((5, 121), ((0, 0), (147, 0), (147, 115), (0, 115))),
        ((0, 119), ((0, 0), (158, 0), (158, 102), (0, 102))),
        ((0, 116), ((0, 0), (158, 0), (158, 107), (0, 107))),
        ((0, 119), ((0, 0), (158, 0), (158, 103), (0, 101))),
        ((2, 101), ((0, 0), (153, 0), (153, 122), (0, 120))),
        ((-18, 85), ((61, 0), (194, 15), (143, 146), (0, 133))),
        ((0, 66), ((88, 1), (173, 17), (123, 182), (0, 131))),
        ((0, 29), ((118, 3), (201, 48), (111, 220), (1, 168))),
    ]
    for i in range(24):
        frame = BuildImage.open(img_dir / f"{i}.png")
        pos, points = params[i]
        frame.paste(img.perspective(points), pos, below=True)
        frames.append(frame.image)

    return save_gif(frames, 0.05)


add_meme(
    "tease",
    tease,
    min_images=1,
    max_images=1,
    keywords=["拿捏", "戏弄"],
    tags=MemeTags.blue_archive,
    date_created=datetime(2023, 6, 27),
    date_modified=datetime(2023, 6, 27),
)
