from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import run_sync, translate


@run_sync
def _dianzhongdian(img: BuildImage, text: str, trans: str):
    img = img.convert("L").resize_width(500)
    text_img1 = BuildImage.new("RGBA", (500, 60))
    text_img2 = BuildImage.new("RGBA", (500, 35))

    try:
        text_img1.draw_text(
            (20, 0, text_img1.width - 20, text_img1.height),
            text,
            max_fontsize=50,
            min_fontsize=25,
            fill="white",
        )
    except ValueError:
        raise TextOverLength(text)

    try:
        text_img2.draw_text(
            (20, 0, text_img2.width - 20, text_img2.height),
            trans,
            max_fontsize=25,
            min_fontsize=10,
            fill="white",
        )
    except ValueError:
        raise TextOverLength(text)

    frame = BuildImage.new("RGBA", (500, img.height + 100), "black")
    frame.paste(img, alpha=True)
    frame.paste(text_img1, (0, img.height), alpha=True)
    frame.paste(text_img2, (0, img.height + 60), alpha=True)
    return frame.save_jpg()


async def dianzhongdian(images: List[BuildImage], texts: List[str], args):
    if len(texts) == 1:
        text = texts[0]
        trans = await translate(text, lang_to="jp")
    else:
        text = texts[0]
        trans = texts[1]

    return await _dianzhongdian(images[0], text, trans)


add_meme(
    "dianzhongdian",
    dianzhongdian,
    min_images=1,
    max_images=1,
    min_texts=1,
    max_texts=2,
    default_texts=["救命啊"],
    keywords=["入典", "典中典", "黑白草图"],
)
