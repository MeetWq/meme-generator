from datetime import datetime
from pathlib import Path
from PIL import Image
from pil_utils import BuildImage
from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif


img_dir = Path(__file__).parent / "images"


def qq_candy(images: list[BuildImage], texts, args):
    positions = [
        # (perspective_points,paste_positon)
        (((72, 0), (72, 75), (0, 75), (0, 0)), (172, 124)),
        (((72, 0), (72, 75), (0, 75), (0, 0)), (172, 124)),
        (((74, 0), (74, 77), (0, 77), (0, 0)), (173, 122)),
        (((72, 0), (72, 76), (0, 76), (0, 0)), (177, 124)),
        (((62, 0), (67, 74), (5, 78), (0, 4)), (184, 120)),
        (((64, 0), (64, 75), (0, 75), (0, 0)), (195, 120)),
        (((58, 0), (58, 74), (0, 74), (0, 0)), (212, 120)),
        (((63, 6), (55, 80), (0, 74), (8, 0)), (238, 120)),
        (((86, 31), (40, 90), (0, 59), (46, 0)), (216, 130)),
        (((91, 38), (30, 86), (0, 48), (61, 0)), (195, 152)),
        (((89, 35), (25, 80), (0, 45), (64, 0)), (160, 156)),
        (((87, 28), (32, 92), (0, 64), (55, 0)), (118, 134)),
        (((73, 16), (36, 98), (0, 82), (37, 0)), (88, 109)),
        (((54, 5), (44, 98), (0, 93), (10, 0)), (71, 89)),
        (((34, 0), (45, 94), (11, 98), (0, 4)), (56, 74)),
        (((33, 0), (59, 97), (26, 106), (0, 9)), (39, 62)),
        (((44, 0), (80, 98), (36, 114), (0, 16)), (24, 54)),
        (((85, 0), (116, 100), (31, 126), (0, 26)), (-1, 46)),
        (((85, 0), (116, 100), (31, 126), (0, 26)), (-1, 46)),
        (((44, 0), (80, 98), (36, 114), (0, 16)), (24, 54)),
        (((44, 0), (80, 98), (36, 114), (0, 16)), (24, 54)),
        (((85, 0), (116, 100), (31, 126), (0, 26)), (-1, 46)),
        (((85, 0), (116, 100), (31, 126), (0, 26)), (-1, 46)),
        (((44, 0), (77, 98), (33, 113), (0, 15)), (20, 45)),
        (((44, 0), (77, 98), (33, 113), (0, 15)), (20, 45)),
        (((85, 0), (116, 100), (31, 126), (0, 26)), (-1, 36)),
        (((85, 0), (116, 100), (31, 126), (0, 26)), (-1, 34)),
        (((44, 0), (77, 98), (33, 113), (0, 15)), (20, 35)),
        (((44, 0), (77, 98), (33, 113), (0, 15)), (20, 35)),
        (((85, 0), (116, 100), (31, 126), (0, 26)), (-1, 28)),
        (((85, 0), (116, 100), (31, 126), (0, 26)), (-1, 28)),
        (((42, 0), (75, 96), (33, 110), (0, 14)), (10, 30)),
        (((34, 0), (67, 96), (33, 108), (0, 12)), (14, 32)),
        (((38, 0), (69, 90), (31, 103), (0, 13)), (14, 37)),
        (((42, 0), (73, 91), (31, 105), (0, 14)), (8, 59)),
        (((48, 0), (76, 84), (28, 100), (0, 16)), (37, 111)),
        (((55, 0), (80, 84), (25, 100), (0, 16)), (76, 125)),
        (((56, 0), (79, 79), (23, 95), (0, 16)), (105, 129)),
        (((59, 0), (82, 76), (23, 94), (0, 18)), (124, 128)),
        (((60, 0), (81, 75), (21, 92), (0, 17)), (139, 125)),
        (((63, 0), (85, 73), (22, 92), (0, 19)), (148, 121)),
        (((62, 0), (82, 73), (20, 90), (0, 17)), (156, 119)),
        (((63, 0), (78, 73), (15, 86), (0, 13)), (163, 120)),
        (((65, 0), (81, 73), (16, 87), (0, 14)), (166, 119)),
        (((55, 0), (66, 77), (11, 85), (0, 8)), (173, 122)),
        (((48, 0), (64, 73), (16, 83), (0, 10)), (172, 122)),
        (((40, 0), (59, 70), (19, 81), (0, 11)), (172, 125)),
        (((27, 0), (48, 70), (21, 78), (0, 8)), (176, 126)),
        (((23, 0), (47, 68), (24, 76), (0, 8)), (176, 128)),
        (((24, 0), (51, 67), (27, 77), (0, 10)), (170, 128)),
        (((23, 0), (57, 65), (34, 77), (0, 12)), (162, 130)),
        (((24, 0), (60, 63), (36, 77), (0, 14)), (156, 132)),
        (((27, 0), (65, 63), (38, 79), (0, 16)), (152, 132)),
        (((37, 0), (77, 63), (40, 86), (0, 23)), (144, 129)),
        (((41, 0), (85, 60), (44, 90), (0, 30)), (135, 132)),
        (((46, 0), (94, 58), (48, 96), (0, 38)), (127, 130)),
        (((60, 0), (103, 61), (43, 103), (0, 42)), (124, 126)),
        (((59, 0), (101, 60), (42, 101), (0, 41)), (126, 126)),
        (((64, 0), (100, 65), (36, 101), (0, 36)), (131, 122)),
        (((61, 0), (96, 67), (35, 99), (0, 32)), (136, 120)),
        (((63, 0), (93, 70), (30, 97), (0, 27)), (143, 119)),
        (((69, 0), (91, 70), (22, 92), (0, 22)), (150, 119)),
        (((67, 0), (83, 72), (16, 87), (0, 15)), (158, 120)),
        (((62, 0), (82, 73), (20, 90), (0, 17)), (156, 119)),
        (((67, 0), (79, 73), (12, 84), (0, 11)), (165, 119)),
        (((65, 0), (81, 73), (16, 87), (0, 14)), (166, 119)),
        (((55, 0), (66, 77), (11, 85), (0, 8)), (173, 122)),
        (((48, 0), (64, 73), (16, 83), (0, 10)), (172, 122)),
        (((40, 0), (59, 70), (19, 81), (0, 11)), (172, 125)),
        (((27, 0), (48, 70), (21, 78), (0, 8)), (176, 126)),
        (((23, 0), (47, 68), (24, 76), (0, 8)), (176, 128)),
        (((24, 0), (51, 67), (27, 77), (0, 10)), (170, 128)),
        (((21, 0), (60, 64), (39, 77), (0, 13)), (155, 132)),
        (((23, 0), (63, 62), (40, 77), (0, 15)), (149, 135)),
        (((31, 0), (72, 62), (41, 82), (0, 20)), (141, 133)),
        (((37, 0), (78, 62), (41, 86), (0, 24)), (136, 133)),
        (((46, 0), (87, 62), (41, 93), (0, 31)), (130, 130)),
        (((52, 0), (93, 62), (41, 97), (0, 35)), (127, 128)),
        (((58, 0), (99, 62), (41, 101), (0, 39)), (127, 124)),
        (((58, 0), (98, 62), (40, 100), (0, 38)), (129, 124)),
        (((60, 0), (95, 65), (35, 97), (0, 32)), (135, 122)),
        (((64, 0), (94, 68), (30, 96), (0, 28)), (143, 118)),
        (((64, 0), (85, 71), (21, 90), (0, 19)), (152, 120)),
        (((69, 0), (83, 73), (14, 86), (0, 13)), (160, 119)),
        (((76, 0), (76, 73), (0, 73), (0, 0)), (172, 125)),
        (((76, 0), (76, 73), (0, 73), (0, 0)), (172, 125)),
        (((76, 0), (76, 73), (0, 73), (0, 0)), (172, 125)),
        (((76, 0), (76, 73), (0, 73), (0, 0)), (172, 125)),
        (((76, 0), (76, 73), (0, 73), (0, 0)), (172, 125)),
        (((76, 0), (76, 73), (0, 73), (0, 0)), (172, 125)),
        (((76, 0), (76, 73), (0, 73), (0, 0)), (172, 125)),
    ]

    def maker(i: int) -> Maker:
        def make(img: BuildImage) -> BuildImage:
            img = (
                img.convert("RGBA")
                .resize((76, 76), keep_ratio=True)
                .circle()
                .rotate(90)
            )
            if i in [19, 20, 27, 28]:
                img = img.transpose(Image.FLIP_TOP_BOTTOM)
            img = img.perspective(positions[i][0])
            bg = BuildImage.open(img_dir / f"{i}.png")
            bg.image.paste(img.image, positions[i][1], img.image)
            return bg

        return make

    return make_gif_or_combined_gif(
        images[0], maker, 91, 0.033, FrameAlignPolicy.extend_first
    )


add_meme(
    "qq_candy",
    qq_candy,
    min_images=1,
    max_images=1,
    keywords=["QQ舔糖"],
    tags=MemeTags.qq,
    date_created=datetime(2024, 8, 14),
    date_modified=datetime(2024, 8, 14),
)
