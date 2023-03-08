from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def cover_face(images: List[BuildImage], texts, args):
    points = ((15, 15), (448, 0), (445, 456), (0, 465))
    img = images[0].convert("RGBA").square().resize((450, 450)).perspective(points)
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img, (120, 150), below=True)
    return frame.save_jpg()


add_meme("cover_face", cover_face, min_images=1, max_images=1, keywords=["捂脸"])
