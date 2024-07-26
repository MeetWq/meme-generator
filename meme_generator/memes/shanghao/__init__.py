from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

img_dir = Path(__file__).parent / "images"


def shanghao(images: list[BuildImage], texts, args):
    params = (
        36 * [(194, 204, 121, 108)]
        + [
            (192, 203, 125, 111),
            (182, 200, 141, 126),
            (161, 188, 178, 159),
            (129, 171, 235, 209),
            (98, 155, 290, 258),
            (98, 155, 290, 258),
            (58, 133, 361, 321),
            (45, 126, 384, 342),
            (45, 126, 384, 342),
            (35, 121, 402, 358),
            (27, 117, 415, 370),
            (17, 111, 433, 386),
            (14, 110, 439, 391),
            (14, 110, 439, 391),
            (11, 108, 444, 395),
            (10, 108, 446, 397),
        ]
        + 8 * [(7, 106, 451, 402)]
    )

    def maker(i: int) -> Maker:
        def make(img: BuildImage) -> BuildImage:
            x, y, w, h = params[i]
            screen = img.convert("RGBA").resize((w, h), keep_ratio=True)
            frame = BuildImage.open(img_dir / f"{i}.png")
            frame.paste(screen, (x, y), below=True)
            return frame

        return make

    return make_gif_or_combined_gif(
        images[0], maker, 60, 0.06, FrameAlignPolicy.extend_last
    )


add_meme("shanghao", shanghao, min_images=1, max_images=1, keywords=["上号"])
