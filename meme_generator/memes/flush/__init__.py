from datetime import datetime
from pathlib import Path
import random

from pil_utils import BuildImage
from PIL import Image

from meme_generator import add_meme
from meme_generator.utils import make_gif_or_combined_gif,Maker,FrameAlignPolicy

img_dir = Path(__file__).parent / "images"


def flush(images: list[BuildImage], texts, args):
    def maker(i:int)->Maker:
        def make(imgs:list[BuildImage]):
            img = imgs[0].convert("RGBA").square().image
            w,h = img.size
            if i >=18:
                return BuildImage.open(img_dir / f"{i-18}.png").resize((w,h),keep_ratio=True)
            else:
                j = 0.2 * (2 * random.random() - 1) #抖动
                k = 8 * i #变红
                f = 0.01 * i #放大
                crop_box = (
                    w*f + w*f*j,
                    h*f + h*f*j,
                    w*(1-f) + w*f*j,
                    h*(1-f) + h*f*j,
                )
                croped_img = img.crop(crop_box)
                frame = Image.new("RGBA",croped_img.size,"white")
                frame.paste(croped_img,(0,0),croped_img)
                red_filter =Image.new("RGBA", croped_img.size, (255, 0, 0,k))
                filtered_image = Image.alpha_composite(frame, red_filter)
                return BuildImage(filtered_image.resize((w,h)))

        return make
    return make_gif_or_combined_gif(
        images,maker,30,0.08,FrameAlignPolicy.no_extend
    )




add_meme(
    "flush",
    flush,
    min_images=1,
    max_images=1,
    keywords=["红温"],
    date_created=datetime(2024, 9, 3),
    date_modified=datetime(2024, 9, 3),
)