from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif


img_dir = Path(__file__).parent / "images"


def boring(images: list[BuildImage], texts, args):
    positions = [
        (0, 118),
        (0, 117),
        (0, 116),
        (0, 116),
        (-3, 116),
        (-7, 117),
        ]
    def maker(i: int) -> Maker:
        def make(img: BuildImage) -> BuildImage:
            img = img.convert("RGBA").resize((100, 100), keep_ratio=True)
            img = img.perspective(((0, 6), (77, -5), (100, 100), (32, 100)))
            bg = BuildImage.open(img_dir / f"{i}.png")
            frame = BuildImage.new("RGBA", (240, 240), "white")
            frame.paste(bg).paste(img,positions[min(max(i-16,0),5)], below=True)
            return frame

        return make

    return make_gif_or_combined_gif(
        images[0], maker, 48, 0.08, FrameAlignPolicy.extend_first
    )


add_meme(
    "boring",
    boring,
    min_images=1,
    max_images=1,
    keywords=["无聊","看困了"],
    tags=MemeTags.mahiro,
    date_created=datetime(2024, 8, 18),
    date_modified=datetime(2024, 8, 18),
)
