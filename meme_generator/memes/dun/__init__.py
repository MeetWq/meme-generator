import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator.tags import MemeTags
from meme_generator import add_meme
from meme_generator.utils import Maker, make_gif_or_combined_gif, FrameAlignPolicy


img_dir = Path(__file__).parent / "images"


def dun(images:list[BuildImage],texts,args):
    def maker(i:int)->Maker:
        def make(imgs:list[BuildImage])->BuildImage:
            img = imgs[0].convert("RGBA").resize((80,80),keep_ratio=True).circle()
            bg = BuildImage.open(img_dir / f"{i}.png").convert("RGBA")
            if i in [2,3,5]:
                y = 45
            else:
                y = 47
            return bg.paste(img,(88, y),below=True)
        return make
    return make_gif_or_combined_gif(images, maker,5,0.08, FrameAlignPolicy.extend_loop)


add_meme(
    "dun",
    dun,
    max_images=1,
    min_images=1,
    tags=MemeTags.capoo,
    keywords=["炖"],
    date_created=datetime.datetime(2024, 8, 21),
    date_modified=datetime.datetime(2024, 8, 21),
)
