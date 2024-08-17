from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

img_dir = Path(__file__).parent / "images"


def shiroko_pero(images: list[BuildImage], texts, args):
    mask = BuildImage.open(img_dir / "mask.png").convert("RGBA")

    def maker(i) -> Maker:
        def make(imgs: list[BuildImage]) -> BuildImage:
            suika = imgs[0].convert("RGBA").resize((245, 245), keep_ratio=True)
            frame = BuildImage.open(img_dir / f"{i}.png").convert("RGBA")
            suika_mask = BuildImage.new("RGBA", (245, 245), (0, 0, 0, 0))
            suika_mask.image.paste(suika.image, (0, 0), mask.image)
            frame.paste(suika_mask, (105, 178), below=True)
            return frame

        return make

    return make_gif_or_combined_gif(
        images, maker, 4, 0.06, FrameAlignPolicy.extend_loop
    )


add_meme(
    "shiroko_pero",
    shiroko_pero,
    min_images=1,
    max_images=1,
    keywords=["白子舔"],
    tags=MemeTags.shiroko,
    date_created=datetime(2024, 8, 10),
    date_modified=datetime(2024, 8, 10),
)
