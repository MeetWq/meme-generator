from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

img_dir = Path(__file__).parent / "images"


def tom_tease(images: list[BuildImage], texts, args):
    def maker(i: int) -> Maker:
        def make(imgs: list[BuildImage]) -> BuildImage:
            img = imgs[0].convert("RGBA").resize((400, 350), keep_ratio=True)
            img = img.perspective(((0, 100), (290, 0), (290, 370), (0, 335)))
            bg = BuildImage.open(img_dir / f"{i}.png")
            frame = BuildImage.new("RGBA", bg.size, "white")
            frame.paste(bg).paste(img, (258, -12), below=True)
            return frame

        return make

    return make_gif_or_combined_gif(
        images, maker, 11, 0.2, FrameAlignPolicy.extend_first
    )


add_meme(
    "tom_tease",
    tom_tease,
    min_images=1,
    max_images=1,
    keywords=["汤姆嘲笑"],
    tags=MemeTags.tom,
    date_created=datetime(2024, 1, 19),
    date_modified=datetime(2024, 1, 19),
)
