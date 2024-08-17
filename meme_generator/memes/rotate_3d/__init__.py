from datetime import datetime

import numpy as np
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif


def rotate_3d(images: list[BuildImage], texts, args):
    tmp_img = images[0].convert("RGBA")
    fov = 45 * np.pi / 180
    z = np.sqrt(tmp_img.width**2 + tmp_img.height**2) / 2 / np.tan(fov / 2)
    w = round(tmp_img.width * 1.2)
    h = round(tmp_img.height * 1.5)
    bg = BuildImage.new("RGBA", (w, h))

    def rotate_y(img: BuildImage, theta: float) -> BuildImage:
        mat = np.array(
            [
                [np.cos(theta), 0, np.sin(theta)],
                [0, 1, 0],
                [-np.sin(theta), 0, np.cos(theta)],
            ]
        )
        pc = np.array([img.width / 2, img.height / 2, 0])
        orgs = [
            np.array([0, 0, 0]),
            np.array([img.width, 0, 0]),
            np.array([img.width, img.height, 0]),
            np.array([0, img.height, 0]),
        ]
        dsts = []
        for i in range(4):
            dst = mat.dot(orgs[i] - pc)
            dsts.append(
                [
                    dst[0] * z / (z - dst[2]) + pc[0],
                    dst[1] * z / (z - dst[2]) + pc[1],
                ]
            )
        min_x = min(dsts, key=lambda x: x[0])[0]
        min_y = min(dsts, key=lambda x: x[1])[1]
        for i in range(4):
            dsts[i][0] -= min_x
            dsts[i][1] -= min_y
        return img.perspective(tuple(dsts))

    def maker(i: int) -> Maker:
        def make(imgs: list[BuildImage]) -> BuildImage:
            img = imgs[0].convert("RGBA")
            frame = bg.copy()
            rotated = rotate_y(img, i * 12 * np.pi / 180)
            frame.paste(
                rotated,
                (
                    round((bg.width - rotated.width) / 2),
                    round((bg.height - rotated.height) / 2),
                ),
                alpha=True,
            )
            return frame

        return make

    return make_gif_or_combined_gif(
        images, maker, 30, 0.07, FrameAlignPolicy.extend_loop
    )


add_meme(
    "rotate_3d",
    rotate_3d,
    min_images=1,
    max_images=1,
    keywords=["三维旋转"],
    date_created=datetime(2024, 4, 30),
    date_modified=datetime(2024, 4, 30),
)
