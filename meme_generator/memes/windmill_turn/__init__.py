from datetime import datetime

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif


def windmill_turn(images: list[BuildImage], texts, args):
    def maker(i: int) -> Maker:
        def make(imgs: list[BuildImage]) -> BuildImage:
            img = imgs[0].convert("RGBA").resize((300, 300), keep_ratio=True)
            frame = BuildImage.new("RGBA", (600, 600), "white")
            frame.paste(img, alpha=True)
            frame.paste(img.rotate(90), (0, 300), alpha=True)
            frame.paste(img.rotate(180), (300, 300), alpha=True)
            frame.paste(img.rotate(270), (300, 0), alpha=True)
            return frame.rotate(i * 18).crop((50, 50, 550, 550))

        return make

    return make_gif_or_combined_gif(
        images, maker, 5, 0.05, FrameAlignPolicy.extend_loop
    )


add_meme(
    "windmill_turn",
    windmill_turn,
    min_images=1,
    max_images=1,
    keywords=["风车转"],
    date_created=datetime(2022, 12, 13),
    date_modified=datetime(2023, 2, 14),
)
