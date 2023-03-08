from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def lim_x_0(images: List[BuildImage], texts, args):
    img = images[0]
    frame = BuildImage.open(img_dir / "0.png")
    img_c = img.convert("RGBA").circle().resize((72, 72))
    img_tp = img.convert("RGBA").circle().resize((51, 51))
    frame.paste(img_tp, (948, 247), alpha=True)
    # fmt: off
    locs = [
        (143, 32), (155, 148), (334, 149), (275, 266), (486, 266),
        (258, 383), (439, 382), (343, 539), (577, 487), (296, 717),
        (535, 717), (64, 896), (340, 896), (578, 897), (210, 1038),
        (644, 1039), (64, 1192), (460, 1192), (698, 1192), (1036, 141),
        (1217, 141), (1243, 263), (1140, 378), (1321, 378), (929, 531),
        (1325, 531), (1592, 531), (1007, 687), (1390, 687), (1631, 686),
        (1036, 840), (1209, 839), (1447, 839), (1141, 1018), (1309, 1019),
        (1546, 1019), (1037, 1197), (1317, 1198), (1555, 1197),
    ]
    # fmt: on
    for i in range(39):
        x, y = locs[i]
        frame.paste(img_c, (x, y), alpha=True)
    return frame.save_jpg()


add_meme("lim_x_0", lim_x_0, min_images=1, max_images=1, keywords=["等价无穷小"])
