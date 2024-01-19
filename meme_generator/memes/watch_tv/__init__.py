from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

img_dir = Path(__file__).parent / "images"


def watch_tv(images: List[BuildImage], texts, args):
    params = (
        (((0, 75), (290, -15), (290, 355), (0, 330)), (347, 3)),
        (((0, 75), (290, -15), (290, 355), (0, 330)), (347, 3)),
        (((0, 75), (290, -15), (290, 355), (0, 330)), (347, 3)),
        (((0, 75), (290, -15), (290, 355), (0, 330)), (347, 3)),
        (((0, 75), (290, -15), (290, 355), (0, 330)), (347, 3)),
        (((0, 75), (290, -15), (290, 355), (0, 330)), (347, 3)),
        (((0, 75), (290, -15), (290, 355), (0, 330)), (347, 3)),
        (((0, 75), (290, -15), (290, 355), (0, 330)), (347, 3)),
        (((0, 75), (290, -15), (290, 355), (0, 330)), (347, 3)),
        (((0, 75), (290, -15), (290, 355), (0, 330)), (347, 3)),
        (((0, 75), (290, -15), (290, 355), (0, 330)), (347, 3)),
        (((0, 75), (290, -15), (290, 355), (0, 330)), (347, 3)),
    )

    def maker(i: int) -> Maker:
        def make(img: BuildImage) -> BuildImage:
            frame = BuildImage.new("RGBA", (720, 405), "white")
            img = images[0].convert("RGBA").resize((291, 355), keep_ratio=True)
            bg = BuildImage.open(img_dir / f"{i}.png")
            frame.paste(bg, (0, 0))
            points, pos = params[i]
            frame.paste(img.perspective(points), pos, below=True)

            return frame

        return make

    return make_gif_or_combined_gif(
        images[0], maker, 11, 0.2, FrameAlignPolicy.extend_first
    )


add_meme("watch_tv", watch_tv, min_images=1, max_images=1, keywords=["汤姆嘲笑", "嘲笑"])
