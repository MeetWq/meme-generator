from datetime import datetime

import numpy as np
from PIL import Image, ImageDraw
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif


def crop_to_triangle(img: BuildImage) -> BuildImage:
    img_w, img_h = img.size
    frame = Image.new("RGBA", img.size, (0, 0, 0, 0))
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.polygon([(img_w // 2, 0), (0, img_h), (img_w, img_h)], fill=255)
    frame.paste(img.image, (0, 0), mask)
    return BuildImage(frame)


def pyramid(images: list[BuildImage], texts, args):
    img_w = 300
    img_h = 300
    fov = 45 * np.pi / 180
    z = np.sqrt(img_w**2 + img_h**2) / 2 / np.tan(fov / 2)
    a = 180
    h = 180
    rh = int(np.sqrt(a**2 + h**2))

    def rotate_y(img: BuildImage, theta: float) -> tuple[tuple[int, int], BuildImage]:
        mat = np.array(
            [
                [np.cos(theta), 0, np.sin(theta)],
                [0, 1, 0],
                [-np.sin(theta), 0, np.cos(theta)],
            ]
        )
        orgs = [
            np.array([-a / 2, -h / 2, 0]),
            np.array([a / 2, -h / 2, 0]),
            np.array([a / 2, h / 2, a / 2]),
            np.array([-a / 2, h / 2, a / 2]),
        ]
        dsts = []
        for i in range(4):
            dst = mat.dot(orgs[i])
            dsts.append(
                [
                    int(dst[0] * z / (z - dst[2])),
                    int(dst[1] * z / (z - dst[2])),
                ]
            )
        min_x = min(dsts, key=lambda x: x[0])[0]
        min_y = min(dsts, key=lambda x: x[1])[1]
        for i in range(4):
            dsts[i][0] -= min_x
            dsts[i][1] -= min_y
        pos = (img_w // 2 + min_x, img_h // 2 + min_y)
        img = img.convert("RGBA").resize((a, rh), keep_ratio=True)
        img = crop_to_triangle(img)
        img = img.perspective(tuple(dsts))
        return pos, img

    if len(images) == 1:
        images.append(images[0])
    frame_num_per_image = 15
    frame_num = len(images) * frame_num_per_image
    theta_step = 90 / frame_num_per_image

    def maker(i: int) -> Maker:
        img_idx1 = i // frame_num_per_image
        img_idx2 = (img_idx1 + 1) % len(images)
        theta1 = i % frame_num_per_image * theta_step
        theta2 = theta1 - 90

        def make(imgs: list[BuildImage]) -> BuildImage:
            frame = BuildImage.new("RGBA", (img_w, img_h))
            pos1, img1 = rotate_y(imgs[img_idx1], theta1 / 180 * np.pi)
            pos2, img2 = rotate_y(imgs[img_idx2], theta2 / 180 * np.pi)
            frame.paste(img2, pos2, alpha=True)
            frame.paste(img1, pos1, alpha=True)
            return frame

        return make

    return make_gif_or_combined_gif(
        images, maker, frame_num, 0.06, FrameAlignPolicy.extend_loop
    )


add_meme(
    "pyramid",
    pyramid,
    min_images=1,
    max_images=4,
    keywords=["四棱锥", "金字塔"],
    date_created=datetime(2024, 8, 16),
    date_modified=datetime(2024, 8, 18),
)
