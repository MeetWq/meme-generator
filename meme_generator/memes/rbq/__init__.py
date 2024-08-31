from datetime import datetime

from pil_utils import BuildImage

from meme_generator import MemeArgsModel, add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif


def rbq(images: list[BuildImage], texts: list[str], args: MemeArgsModel):
    img_w, img_h = images[0].convert("RGBA").resize_width(500).size
    frame = BuildImage.new("RGBA", (600, img_h + 230), "white")
    text = "非常可爱！简直就是"
    frame.draw_text(
         (0, img_h + 120, 480, img_h + 185), text, max_fontsize=48, weight="bold", fill=(0, 0, 0)
    )
    
    text = "RBQ"
    frame.draw_text(
        (440, img_h + 120, 570, img_h + 185), text, max_fontsize=48, weight="bold", fill=(255, 0, 0)
    )
    text = f"她没失踪也没怎么样  我只是觉得你们都该玩一下"
    frame.draw_text(
        (20, img_h + 180, 580, img_h + 215), text,  max_fontsize=26, fill=(0, 0, 0)
    )

    name = "她"
    if texts:
        name = texts[0]
   

    text = f"请问你们看到{name}了吗?"
    try:
        frame.draw_text(
            (20, 0, 580, 110), text, max_fontsize=70, min_fontsize=25, weight="bold"
        )
    except ValueError:
        raise TextOverLength(name)

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize_width(500)
        return frame.copy().paste(img, (int(300 - img_w / 2), 110), alpha=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "rbq",
    rbq,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    keywords=["rbq", "惹不起"],
    date_created=datetime(2022, 1, 1),
    date_modified=datetime(2023, 2, 14),
)
