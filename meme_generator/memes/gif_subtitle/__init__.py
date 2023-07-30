from pathlib import Path
from typing import List, Tuple

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def make_gif(
    key: str,
    texts: List[str],
    pieces: Tuple[Tuple[int, int], ...],
    fontsize: int = 20,
    padding_x: int = 5,
    padding_y: int = 5,
):
    img = BuildImage.open(img_dir / f"{key}.gif").image
    frames: List[BuildImage] = []
    for i in range(img.n_frames):
        img.seek(i)
        frames.append(BuildImage(img.convert("RGB")))

    parts = [frames[start:end] for start, end in pieces]
    for part, text in zip(parts, texts):
        for frame in part:
            try:
                frame.draw_text(
                    (padding_x, 0, frame.width - padding_x, frame.height - padding_y),
                    text,
                    max_fontsize=fontsize,
                    min_fontsize=fontsize,
                    fill="white",
                    stroke_ratio=0.05,
                    stroke_fill="black",
                    valign="bottom",
                )
            except ValueError:
                raise TextOverLength(text)

    return save_gif([frame.image for frame in frames], img.info["duration"] / 1000)


def add_gif_meme(
    key: str,
    keywords: List[str],
    pieces: Tuple[Tuple[int, int], ...],
    examples: Tuple[str, ...],
    **kwargs,
):
    def gif_func(images, texts: List[str], args):
        return make_gif(key, texts, pieces, **kwargs)

    text_num = len(pieces)
    add_meme(
        key,
        gif_func,
        min_texts=text_num,
        max_texts=text_num,
        default_texts=list(examples),
        keywords=keywords,
    )


add_gif_meme(
    "wangjingze",
    ["王境泽"],
    ((0, 9), (12, 24), (25, 35), (37, 48)),
    ("我就是饿死", "死外边 从这里跳下去", "不会吃你们一点东西", "真香"),
)

# fmt: off
add_gif_meme(
    "weisuoyuwei",
    ["为所欲为"],
    ((11, 14), (27, 38), (42, 61), (63, 81), (82, 95), (96, 105), (111, 131), (145, 157), (157, 167),),
    ("好啊", "就算你是一流工程师", "就算你出报告再完美", "我叫你改报告你就要改", "毕竟我是客户", "客户了不起啊", "Sorry 客户真的了不起", "以后叫他天天改报告", "天天改 天天改"),
    fontsize=19,
)
# fmt: on

add_gif_meme(
    "chanshenzi",
    ["馋身子"],
    ((0, 16), (16, 31), (33, 40)),
    ("你那叫喜欢吗？", "你那是馋她身子", "你下贱！"),
    fontsize=18,
)

add_gif_meme(
    "qiegewala",
    ["切格瓦拉"],
    ((0, 15), (16, 31), (31, 38), (38, 48), (49, 68), (68, 86)),
    ("没有钱啊 肯定要做的啊", "不做的话没有钱用", "那你不会去打工啊", "有手有脚的", "打工是不可能打工的", "这辈子不可能打工的"),
)

add_gif_meme(
    "shuifandui",
    ["谁反对"],
    ((3, 14), (21, 26), (31, 38), (40, 45)),
    ("我话说完了", "谁赞成", "谁反对", "我反对"),
    fontsize=19,
)

add_gif_meme(
    "zengxiaoxian",
    ["曾小贤"],
    ((3, 15), (24, 30), (30, 46), (56, 63)),
    ("平时你打电子游戏吗", "偶尔", "星际还是魔兽", "连连看"),
    fontsize=21,
)

add_gif_meme(
    "yalidaye",
    ["压力大爷"],
    ((0, 16), (21, 47), (52, 77)),
    ("外界都说我们压力大", "我觉得吧压力也没有那么大", "主要是28岁了还没媳妇儿"),
    fontsize=21,
)

add_gif_meme(
    "nihaosaoa",
    ["你好骚啊"],
    ((0, 14), (16, 26), (42, 61)),
    ("既然追求刺激", "就贯彻到底了", "你好骚啊"),
    fontsize=17,
)

add_gif_meme(
    "shishilani",
    ["食屎啦你"],
    ((14, 21), (23, 36), (38, 46), (60, 66)),
    ("穿西装打领带", "拿大哥大有什么用", "跟着这样的大哥", "食屎啦你"),
    fontsize=17,
)

add_gif_meme(
    "wunian",
    ["五年怎么过的"],
    ((11, 20), (35, 50), (59, 77), (82, 95)),
    ("五年", "你知道我这五年是怎么过的吗", "我每天躲在家里玩贪玩蓝月", "你知道有多好玩吗"),
    fontsize=16,
)

add_gif_meme(
    "maikease",
    ["麦克阿瑟说"],
    ((0, 22), (24, 46), (48, 70), (72, 84)),
    ("美国前五星上将麦克阿瑟", "曾这样评价道", "如果让我去阻止xxx", "那么我宁愿去阻止上帝"),
)
