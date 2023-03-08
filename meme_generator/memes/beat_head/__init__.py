from typing import List
from pathlib import Path
from pil_utils import BuildImage
from PIL.Image import Image as IMG
from meme_generator.exception import TextOverLength
from meme_generator import add_meme
from meme_generator.utils import save_gif


img_dir = Path(__file__).parent / "images"


def beat_head(images: List[BuildImage], texts: List[str], args):
    text = "怎么说话的你" if not len(texts) else texts[0]
    self_locs = [(160, 121), (172, 124), (208, 166)]
    self_size = [(76,76),(69,69),(52,52)]
    head_img = images[0].convert("RGBA")
    frames: List[IMG] = []
    for i in range(3):
        self_head = head_img.resize(self_size[i]).circle()
        frame = BuildImage.open(img_dir / f"{i}.png")
        try:
            frame.paste(self_head, self_locs[i], alpha=True)   
        except ValueError:
            raise TextOverLength(text)
        frame.draw_text((175,28,316,82),text,max_fontsize=50,min_fontsize=10,allow_wrap=True)
        frames.append(frame.image)  
    return save_gif(frames, 0.05) 




add_meme("beat_head", beat_head, min_images=1, max_images=1,min_texts=0,max_texts=1, keywords=["拍头"])