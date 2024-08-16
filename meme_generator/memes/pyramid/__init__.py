from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif


def crop_to_isosceles_triangle(image: BuildImage) -> BuildImage:
    img_width, img_height = image.size
    triangle_image = Image.new("RGBA", (img_width, img_height), (0, 0, 0, 0))

    top_vertex = (img_width // 2, 0)
    bottom_left_vertex = (0, img_height)
    bottom_right_vertex = (img_width, img_height)
    mask = Image.new("L", (img_width, img_height), 0)

    draw = ImageDraw.Draw(mask)
    draw.polygon([top_vertex, bottom_left_vertex, bottom_right_vertex], fill=255)
    triangle_image.paste(image.image, (0, 0), mask)
    return BuildImage(triangle_image)

def pyramid(images: list[BuildImage], texts, args):
    #右侧三角形
    params1 = [
        (((0, 0), (144, 0), (148, 136), (4, 136)), (24, 32)),
        (((0, 5), (140, 0), (152, 136), (12, 141)), (26, 29)),
        (((0, 8), (135, 0), (155, 135), (20, 143)), (28, 28)),
        (((0, 10), (128, 0), (155, 134), (27, 144)), (32, 27)),
        (((0, 13), (115, 0), (149, 134), (34, 147)), (38, 25)),
        (((0, 15), (103, 0), (144, 134), (41, 149)), (44, 24)),
        (((0, 15), (90, 0), (137, 134), (47, 149)), (51, 24)),
        (((0, 16), (72, 0), (124, 131), (52, 147)), (60, 24)),
        (((0, 18), (56, 0), (112, 131), (56, 149)), (68, 23)),
        (((0, 18), (38, 0), (98, 130), (60, 148)), (77, 23)),
        (((0, 18), (22, 0), (85, 129), (63, 147)), (85, 23)),
        (((0, 16), (3, 0), (69, 128), (66, 144)), (94, 24))
        ]
    #左侧三角形
    params2 = [
        None,
        (((61, 0), (68, 16), (7, 146), (0, 130)), (31, 24)),
        (((59, 0), (82, 16), (23, 147), (0, 131)), (25, 24)),
        (((57, 0), (97, 15), (40, 147), (0, 132)), (19, 24)),
        (((53, 0), (111, 15), (58, 148), (0, 133)), (14, 24)),
        (((48, 0), (122, 15), (74, 149), (0, 134)), (11, 24)),
        (((42, 0), (131, 14), (89, 148), (0, 134)), (9, 25)),
        (((36, 0), (140, 11), (104, 145), (0, 134)), (8, 26)),
        (((30, 0), (146, 10), (116, 145), (0, 135)), (8, 27)),
        (((23, 0), (151, 7), (128, 143), (0, 136)), (9, 28)),
        (((15, 0), (150, 5), (135, 141), (0, 136)), (13, 29)),
        (((7, 0), (150, 1), (143, 137), (0, 136)), (17, 31))
        ]
    result = []
    def make_pyramid(img1:BuildImage,img2:BuildImage)->BuildImage:
        result = []
        for i in range(11):
            bg = BuildImage.new("RGBA", (200, 200))
            triangle1 = crop_to_isosceles_triangle(img1.copy()).perspective(params1[i][0])
            bg.paste(triangle1, params1[i][1])
            if i:
                triangle2 = crop_to_isosceles_triangle(img2.copy()).perspective(params2[i][0])
                bg.image.paste(triangle2.image, params2[i][1],triangle2.image)
            result.append(bg.image)
        return result
    if len(images) == 1:
        result = make_pyramid(images[0],images[0])
    else:
        image = images[0]
        while len(images) >= 2:
            result.extend(make_pyramid(images.pop(0),images[0]))
        result.extend(make_pyramid(images[0],image))
    return save_gif(result,0.04)


add_meme(
    "pyramid",
    pyramid,
    min_images=1,
    max_images=99,
    keywords=["旋转棱锥"],
    date_created=datetime(2024,8, 16),
    date_modified=datetime(2024,8, 16),
)
