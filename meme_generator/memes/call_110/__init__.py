from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme


def call_110(images: List[BuildImage], texts, args):
    img1 = images[0].convert("RGBA").square().resize((250, 250))
    img0 = images[1].convert("RGBA").square().resize((250, 250))

    frame = BuildImage.new("RGB", (900, 500), "white")
    frame.draw_text((0, 0, 900, 200), "遇到困难请拨打", max_fontsize=100)
    frame.paste(img1, (50, 200), alpha=True)
    frame.paste(img1, (325, 200), alpha=True)
    frame.paste(img0, (600, 200), alpha=True)
    return frame.save_jpg()


add_meme("call_110", call_110, min_images=2, max_images=2, keywords=["遇到困难请拨打"])
