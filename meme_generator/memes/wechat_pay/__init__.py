from pathlib import Path
from meme_generator import add_meme
from pil_utils import BuildImage

img_dir = Path(__file__).parent / "images"

def wechat_pay(images: list[BuildImage], texts, args):
    
    user_head = (
        images[0]
        .convert("RGBA")  
        .resize((100, 90), keep_ratio=True) 
    )

    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(user_head, (55, 80), alpha=True)  

    return frame.save_png()  

add_meme(
    "wechat_pay",
    wechat_pay,
    min_images=1,
    max_images=1,
    keywords=["微信支付"],
)
