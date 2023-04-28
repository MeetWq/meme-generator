from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def capoo_rip(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").resize((150, 100), keep_ratio=True)
    img_left = img.crop((0, 0, 75, 100))
    img_right = img.crop((75, 0, 150, 100))
    params1 = [
        [(61, 196), ((140, 68), (0, 59), (33, 0), (165, 8))],
        [(63, 196), ((136, 68), (0, 59), (29, 0), (158, 13))],
        [(62, 195), ((137, 72), (0, 58), (27, 0), (167, 11))],
        [(95, 152), ((0, 8), (155, 0), (163, 107), (13, 112))],
        [(108, 129), ((0, 6), (128, 0), (136, 113), (10, 117))],
        [(84, 160), ((0, 6), (184, 0), (190, 90), (10, 97))],
    ]
    params2 = [
        (
            [(78, 158), ((0, 3), (86, 0), (97, 106), (16, 106))],
            [(195, 156), ((0, 4), (82, 0), (85, 106), (15, 110))],
        ),
        (
            [(89, 156), ((0, 0), (80, 0), (94, 100), (14, 100))],
            [(192, 151), ((0, 7), (79, 3), (82, 107), (11, 112))],
        ),
    ]
    raw_frames = [BuildImage.open(img_dir / f"{i}.png") for i in range(8)]
    for i in range(6):
        pos, points = params1[i]
        raw_frames[i].paste(img.perspective(points), pos, below=True)
    for i in range(2):
        (pos1, points1), (pos2, points2) = params2[i]
        raw_frames[i + 6].paste(img_left.perspective(points1), pos1, below=True)
        raw_frames[i + 6].paste(img_right.perspective(points2), pos2, below=True)

    new_frames: List[BuildImage] = []
    for i in range(3):
        new_frames += raw_frames[0:3]
    new_frames += raw_frames[3:]
    new_frames.append(raw_frames[-1])

    frames = [frame.image for frame in new_frames]
    return save_gif(frames, 0.1)


add_meme(
    "capoo_rip",
    capoo_rip,
    min_images=1,
    max_images=1,
    keywords=["咖波撕"],
)
