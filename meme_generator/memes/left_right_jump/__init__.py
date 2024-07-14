from PIL.Image import Transpose
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif


def left_right_jump(images: list[BuildImage], texts, args):
    img_w = 100
    img_h = images[0].resize_width(img_w).height
    frame_w = 300
    frame_h = img_h + 30
    frame = BuildImage.new("RGBA", (frame_w, frame_h))

    def traj(x: float) -> float:
        h = 15
        w = (frame_w - img_w) / 4
        k = h / w**2
        if x < img_w / 2 or x > frame_w - img_w / 2:
            return 0
        elif x < frame_w / 2:
            return h - k * (x - img_w / 2 - w) ** 2
        else:
            return h - k * (x - img_w / 2 - w * 3) ** 2

    frame_num = 30
    dx = (frame_w - img_w) / (frame_num / 2 - 1)

    def maker(i: int) -> Maker:
        def make(img: BuildImage) -> BuildImage:
            img = images[0].convert("RGBA").resize_width(img_w)
            if i >= round(frame_num / 2):
                x = frame_w - img_w - dx * (frame_num - i - 1)
                img = img.transpose(Transpose.FLIP_LEFT_RIGHT)
            else:
                x = frame_w - img_w - dx * i
            y = frame_h - (traj(x + img_w / 2) + img_h)
            return frame.copy().paste(img, (round(x), round(y)), alpha=True)

        return make

    return make_gif_or_combined_gif(
        images[0], maker, frame_num, 0.04, FrameAlignPolicy.extend_loop
    )


add_meme(
    "left_right_jump",
    left_right_jump,
    min_images=1,
    max_images=1,
    keywords=["左右横跳"],
)
