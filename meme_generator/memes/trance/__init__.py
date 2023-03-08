from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme


def trance(images: List[BuildImage], texts, args):
    img = images[0]
    width, height = img.size
    height1 = int(1.1 * height)
    frame = BuildImage.new("RGB", (width, height1), "white")
    frame.paste(img, (0, int(height * 0.1)))
    img.image.putalpha(3)
    for i in range(int(height * 0.1), 0, -1):
        frame.paste(img, (0, i), alpha=True)
    for i in range(int(height * 0.1), int(height * 0.1 * 2)):
        frame.paste(img, (0, i), alpha=True)
    frame = frame.crop((0, int(0.1 * height), width, height1))
    return frame.save_jpg()


add_meme("trance", trance, min_images=1, max_images=1, keywords=["恍惚"])
