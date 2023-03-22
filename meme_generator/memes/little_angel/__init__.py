from typing import List

from pil_utils import BuildImage

from meme_generator import MemeArgsModel, add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif


def little_angel(images: List[BuildImage], texts: List[str], args: MemeArgsModel):
    img_w, img_h = images[0].convert("RGBA").resize_width(500).size
    frame = BuildImage.new("RGBA", (600, img_h + 230), "white")
    text = "非常可爱！简直就是小天使"
    frame.draw_text(
        (10, img_h + 120, 590, img_h + 185), text, max_fontsize=48, weight="bold"
    )

    ta = "她"
    name = ta
    if texts:
        name = texts[0]
    elif args.user_infos:
        info = args.user_infos[0]
        ta = "他" if info.gender == "male" else "她"
        name = info.name or ta

    text = f"{ta}没失踪也没怎么样  我只是觉得你们都该看一下"
    frame.draw_text(
        (20, img_h + 180, 580, img_h + 215), text, max_fontsize=26, weight="bold"
    )

    text = f"请问你们看到{name}了吗?"
    try:
        frame.draw_text(
            (20, 0, 580, 110), text, max_fontsize=70, min_fontsize=25, weight="bold"
        )
    except ValueError:
        raise TextOverLength(name)

    def make(img: BuildImage) -> BuildImage:
        img = img.convert("RGBA").resize_width(500)
        return frame.copy().paste(img, (int(300 - img_w / 2), 110), alpha=True)

    return make_jpg_or_gif(images[0], make)


add_meme(
    "little_angel",
    little_angel,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    keywords=["小天使"],
)
