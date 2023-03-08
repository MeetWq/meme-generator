import math
import random
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage, Text2Image

from meme_generator import add_meme
from meme_generator.utils import save_gif


def douyin(images, texts: List[str], args):
    text = texts[0]
    text = " ".join(text.splitlines())
    fontsize = 200
    offset = round(fontsize * 0.05)
    px = 70
    py = 30
    bg_color = "#1C0B1B"
    frame = Text2Image.from_text(
        text, fontsize, fill="#FF0050", stroke_fill="#FF0050", stroke_width=5
    ).to_image(bg_color=bg_color, padding=(px + offset * 2, py + offset * 2, px, py))
    Text2Image.from_text(
        text, fontsize, fill="#00F5EB", stroke_fill="#00F5EB", stroke_width=5
    ).draw_on_image(frame, (px, py))
    Text2Image.from_text(
        text, fontsize, fill="white", stroke_fill="white", stroke_width=5
    ).draw_on_image(frame, (px + offset, py + offset))
    frame = BuildImage(frame)

    width = frame.width - px
    height = frame.height - py
    frame_num = 10
    devide_num = 6
    seed = 20 * 0.05
    frames: List[IMG] = []
    for _ in range(frame_num):
        new_frame = frame.copy()
        h_seeds = [
            math.fabs(math.sin(random.random() * devide_num)) for _ in range(devide_num)
        ]
        h_seed_sum = sum(h_seeds)
        h_seeds = [s / h_seed_sum for s in h_seeds]
        direction = 1
        last_yn = 0
        last_h = 0
        for i in range(devide_num):
            yn = last_yn + last_h
            h = max(round(height * h_seeds[i]), 2)
            last_yn = yn
            last_h = h
            direction = -direction
            piece = new_frame.copy().crop((px, yn, px + width, yn + h))
            new_frame.paste(piece, (px + round(i * direction * seed), yn))
        # 透视变换
        move_x = 64
        points = (
            (move_x, 0),
            (new_frame.width + move_x, 0),
            (new_frame.width, new_frame.height),
            (0, new_frame.height),
        )
        new_frame = new_frame.perspective(points)
        bg = BuildImage.new("RGBA", new_frame.size, bg_color)
        bg.paste(new_frame, alpha=True)
        frames.append(bg.image)

    return save_gif(frames, 0.2)


add_meme(
    "douyin",
    douyin,
    min_texts=1,
    max_texts=1,
    default_texts=["douyin"],
    keywords=["douyin"],
)
