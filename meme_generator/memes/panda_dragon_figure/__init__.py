from pathlib import Path
import re

from pil_utils import BuildImage
from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"

def panda_dragon_figure(images, texts: list[str], args):

    frame = BuildImage.open(img_dir / "0.png")

    text = texts[0].strip() 
    match = re.search(r"([^ ]*龙)", text)  
    if match:
        dragon_text = match.group(1)
        text = text.replace(dragon_text, "")
    else:
        dragon_text = "责怪龙"

    try:
        frame.draw_text(
            (140, 460), 
            dragon_text, 
            allow_wrap=True, 
            lines_align="center", 
            fontsize=60, 
            fill=(255, 255, 255)  
        )
    except ValueError:
        raise TextOverLength(dragon_text) 

    if text:
        try:
            frame.draw_text(
                (0, 0, 550, 120), 
                text,
                allow_wrap=True,  
                lines_align="center", 
                max_fontsize=100, 
                min_fontsize=20, 
                fill=(0, 0, 0)  
            )
        except ValueError:
            raise TextOverLength(text)

    return frame.save_png()

add_meme(
    "panda_dragon_figure", 
    panda_dragon_figure, 
    min_texts=1, 
    max_texts=1,
    keywords=["熊猫龙图"]
)
