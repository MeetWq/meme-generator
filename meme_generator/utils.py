import asyncio
import hashlib
import inspect
import math
import random
import time
from collections.abc import Coroutine
from dataclasses import dataclass, field
from enum import Enum
from functools import partial, wraps
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Literal, Protocol, TypeVar

import httpx
from PIL.Image import Image as IMG
from pil_utils import BuildImage, Text2Image
from pil_utils.types import ColorType
from typing_extensions import ParamSpec

from .config import meme_config
from .exception import MemeFeedback

if TYPE_CHECKING:
    from .meme import Meme

resources_dir = Path(__file__).parent / "resources"


P = ParamSpec("P")
R = TypeVar("R")


def run_sync(call: Callable[P, R]) -> Callable[P, Coroutine[None, None, R]]:
    """一个用于包装 sync function 为 async function 的装饰器
    参数:
        call: 被装饰的同步函数
    """

    @wraps(call)
    async def _wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        loop = asyncio.get_running_loop()
        pfunc = partial(call, *args, **kwargs)
        result = await loop.run_in_executor(None, pfunc)
        return result

    return _wrapper


def is_coroutine_callable(call: Callable[..., Any]) -> bool:
    """检查 call 是否是一个 callable 协程函数"""
    if inspect.isroutine(call):
        return inspect.iscoroutinefunction(call)
    if inspect.isclass(call):
        return False
    func_ = getattr(call, "__call__", None)
    return inspect.iscoroutinefunction(func_)


def save_gif(frames: list[IMG], duration: float) -> BytesIO:
    output = BytesIO()
    frames[0].save(
        output,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=duration * 1000,
        loop=0,
        disposal=2,
        optimize=False,
    )

    # 没有超出最大大小，直接返回
    nbytes = output.getbuffer().nbytes
    if nbytes <= meme_config.gif.gif_max_size * 10**6:
        return output

    # 超出最大大小，帧数超出最大帧数时，缩减帧数
    n_frames = len(frames)
    gif_max_frames = meme_config.gif.gif_max_frames
    if n_frames > gif_max_frames:
        index = range(n_frames)
        ratio = n_frames / gif_max_frames
        index = (int(i * ratio) for i in range(gif_max_frames))
        new_duration = duration * ratio
        new_frames = [frames[i] for i in index]
        return save_gif(new_frames, new_duration)

    # 超出最大大小，帧数没有超出最大帧数时，缩小尺寸
    new_frames = [
        frame.resize((int(frame.width * 0.9), int(frame.height * 0.9)))
        for frame in frames
    ]
    return save_gif(new_frames, duration)


class Maker(Protocol):
    def __call__(self, img: BuildImage) -> BuildImage: ...


class GifMaker(Protocol):
    def __call__(self, i: int) -> Maker: ...


def get_avg_duration(image: IMG) -> float:
    if not getattr(image, "is_animated", False):
        return 0
    total_duration = 0
    n_frames = getattr(image, "n_frames", 1)
    for i in range(n_frames):
        image.seek(i)
        total_duration += image.info["duration"]
    return total_duration / n_frames


def split_gif(image: IMG) -> list[IMG]:
    frames: list[IMG] = []
    n_frames = getattr(image, "n_frames", 1)
    for i in range(n_frames):
        image.seek(i)
        frame = image.copy()
        frames.append(frame)
    image.seek(0)
    if image.info.__contains__("transparency"):
        frames[0].info["transparency"] = image.info["transparency"]
    return frames


def make_jpg_or_gif(
    img: BuildImage, func: Maker, keep_transparency: bool = False
) -> BytesIO:
    """
    制作静图或者动图
    :params
      * ``img``: 输入图片
      * ``func``: 图片处理函数，输入img，返回处理后的图片
      * ``keep_transparency``: 传入gif时，是否保留该gif的透明度
    """
    image = img.image
    if not getattr(image, "is_animated", False):
        return func(img).save_jpg()
    else:
        frames = split_gif(image)
        duration = get_avg_duration(image) / 1000
        frames = [func(BuildImage(frame)).image for frame in frames]
        if keep_transparency:
            image.seek(0)
            if image.info.__contains__("transparency"):
                frames[0].info["transparency"] = image.info["transparency"]
        return save_gif(frames, duration)


def make_png_or_gif(
    img: BuildImage, func: Maker, keep_transparency: bool = False
) -> BytesIO:
    """
    制作静图或者动图
    :params
      * ``img``: 输入图片
      * ``func``: 图片处理函数，输入img，返回处理后的图片
      * ``keep_transparency``: 传入gif时，是否保留该gif的透明度
    """
    image = img.image
    if not getattr(image, "is_animated", False):
        return func(img).save_png()
    else:
        frames = split_gif(image)
        duration = get_avg_duration(image) / 1000
        frames = [func(BuildImage(frame)).image for frame in frames]
        if keep_transparency:
            image.seek(0)
            if image.info.__contains__("transparency"):
                frames[0].info["transparency"] = image.info["transparency"]
        return save_gif(frames, duration)


class FrameAlignPolicy(Enum):
    """
    要叠加的gif长度大于基准gif时，是否延长基准gif长度以对齐两个gif
    """

    no_extend = 0
    """不延长"""
    extend_first = 1
    """延长第一帧"""
    extend_last = 2
    """延长最后一帧"""
    extend_loop = 3
    """以循环方式延长"""


def make_gif_or_combined_gif(
    img: BuildImage,
    maker: GifMaker,
    frame_num: int,
    duration: float,
    frame_align: FrameAlignPolicy = FrameAlignPolicy.no_extend,
    input_based: bool = False,
    keep_transparency: bool = False,
) -> BytesIO:
    """
    使用静图或动图制作gif
    :params
      * ``img``: 输入图片，如头像
      * ``maker``: 图片处理函数生成，传入第几帧，返回对应的图片处理函数
      * ``frame_num``: 目标gif的帧数
      * ``duration``: 相邻帧之间的时间间隔，单位为秒
      * ``frame_align``: 要叠加的gif长度大于基准gif时，gif长度对齐方式
      * ``input_based``: 是否以输入gif为基准合成gif，默认为`False`，即以目标gif为基准
      * ``keep_transparency``: 传入gif时，是否保留该gif的透明度
    """
    image = img.image
    if not getattr(image, "is_animated", False):
        return save_gif([maker(i)(img).image for i in range(frame_num)], duration)

    frame_num_in = getattr(image, "n_frames", 1)
    duration_in = get_avg_duration(image) / 1000
    total_duration_in = frame_num_in * duration_in
    total_duration = frame_num * duration

    if input_based:
        frame_num_base = frame_num_in
        frame_num_fit = frame_num
        duration_base = duration_in
        duration_fit = duration
        total_duration_base = total_duration_in
        total_duration_fit = total_duration
    else:
        frame_num_base = frame_num
        frame_num_fit = frame_num_in
        duration_base = duration
        duration_fit = duration_in
        total_duration_base = total_duration
        total_duration_fit = total_duration_in

    frame_idxs: list[int] = list(range(frame_num_base))
    diff_duration = total_duration_fit - total_duration_base
    diff_num = int(diff_duration / duration_base)

    if diff_duration >= duration_base:
        if frame_align == FrameAlignPolicy.extend_first:
            frame_idxs = [0] * diff_num + frame_idxs

        elif frame_align == FrameAlignPolicy.extend_last:
            frame_idxs += [frame_num_base - 1] * diff_num

        elif frame_align == FrameAlignPolicy.extend_loop:
            frame_num_total = frame_num_base
            # 重复基准gif，直到两个gif总时长之差在1个间隔以内，或总帧数超出最大帧数
            while frame_num_total + frame_num_base <= meme_config.gif.gif_max_frames:
                frame_num_total += frame_num_base
                frame_idxs += list(range(frame_num_base))
                multiple = round(frame_num_total * duration_base / total_duration_fit)
                if (
                    math.fabs(
                        total_duration_fit * multiple - frame_num_total * duration_base
                    )
                    <= duration_base
                ):
                    break

    frames: list[IMG] = []
    frame_idx_fit = 0
    time_start = 0
    for i, idx in enumerate(frame_idxs):
        while frame_idx_fit < frame_num_fit:
            if (
                frame_idx_fit * duration_fit
                <= i * duration_base - time_start
                < (frame_idx_fit + 1) * duration_fit
            ):
                if input_based:
                    idx_in = idx
                    idx_maker = frame_idx_fit
                else:
                    idx_in = frame_idx_fit
                    idx_maker = idx

                func = maker(idx_maker)
                image.seek(idx_in)
                frames.append(func(BuildImage(image.copy())).image)
                break
            else:
                frame_idx_fit += 1
                if frame_idx_fit >= frame_num_fit:
                    frame_idx_fit = 0
                    time_start += total_duration_fit

    if keep_transparency:
        image.seek(0)
        if image.info.__contains__("transparency"):
            frames[0].info["transparency"] = image.info["transparency"]

    return save_gif(frames, duration)


def translate(text: str, lang_from: str = "auto", lang_to: str = "zh") -> str:
    appid = meme_config.translate.baidu_trans_appid
    apikey = meme_config.translate.baidu_trans_apikey
    if not appid or not apikey:
        raise MemeFeedback(
            '"baidu_trans_appid" 或 "baidu_trans_apikey" 未设置，请检查配置文件！'
        )
    salt = str(round(time.time() * 1000))
    sign_raw = appid + text + salt + apikey
    sign = hashlib.md5(sign_raw.encode("utf8")).hexdigest()
    params = {
        "q": text,
        "from": lang_from,
        "to": lang_to,
        "appid": appid,
        "salt": salt,
        "sign": sign,
    }
    url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
    resp = httpx.get(url, params=params)
    result = resp.json()
    return result["trans_result"][0]["dst"]


def random_text() -> str:
    return random.choice(
        ["刘一", "陈二", "张三", "李四", "王五", "赵六", "孙七", "周八", "吴九", "郑十"]
    )


def random_image() -> bytes:
    return random.choice(
        list((resources_dir / "images" / "emojis").glob("*.png"))
    ).read_bytes()


@dataclass
class MemeProperties:
    disabled: bool = False
    labels: list[Literal["new", "hot"]] = field(default_factory=list)


def render_meme_list(
    meme_list: list[tuple["Meme", MemeProperties]],
    *,
    text_template: str = "{keywords}",
    add_category_icon: bool = True,
) -> BytesIO:
    TEXT_COLOR_NORMAL = "#444444"
    TEXT_COLOR_DISABLED = "#d3d3d3"
    BLOCK_COLOR_1 = "#f5f5f5"
    BLOCK_COLOR_2 = "#ffffff"
    BG_COLOR = "#fdfcf8"
    FONTSIZE = 30
    BLOCK_HEIGHT = 50

    icon_dir = resources_dir / "images" / "icons"
    category_image = BuildImage.open(icon_dir / "image.png").resize((30, 30))
    category_text = BuildImage.open(icon_dir / "text.png").resize((30, 30))
    category_image_disabled = BuildImage.open(icon_dir / "image_disabled.png").resize(
        (30, 30)
    )
    category_text_disabled = BuildImage.open(icon_dir / "text_disabled.png").resize(
        (30, 30)
    )
    label_new = BuildImage.open(icon_dir / "new.png").resize((30, 30))
    label_hot = BuildImage.open(icon_dir / "hot.png").resize((30, 30))

    def meme_text(number: int, meme: "Meme") -> str:
        return text_template.format(
            index=number + 1,
            key=meme.key,
            keywords="/".join(meme.keywords),
            shortcuts="/".join(
                shortcut.humanized or shortcut.key for shortcut in meme.shortcuts
            ),
            tags="/".join(meme.tags),
        )

    def text_block(
        text: str,
        max_width: int,
        block_color: ColorType,
        properties: MemeProperties,
        category: Literal["text", "image"] = "text",
    ) -> BuildImage:
        image = BuildImage.new("RGBA", (max_width, BLOCK_HEIGHT), block_color)
        if category == "text":
            icon = category_text_disabled if properties.disabled else category_text
        else:
            icon = category_image_disabled if properties.disabled else category_image
        x = 0
        if add_category_icon:
            image.paste(icon, (x + 10, 10), alpha=True)
            x += 50
        text_color = TEXT_COLOR_DISABLED if properties.disabled else TEXT_COLOR_NORMAL
        t2m = Text2Image.from_text(text, fontsize=FONTSIZE, fill=text_color)
        t2m.draw_on_image(image.image, (x + 5, (image.height - t2m.height) // 2))
        x += t2m.width + 10
        if "new" in properties.labels:
            image.paste(label_new, (x + 5, 10), alpha=True)
            x += 35
        if "hot" in properties.labels:
            image.paste(label_hot, (x + 5, 10), alpha=True)
            x += 35
        return image

    meme_num = len(meme_list)
    cols = math.ceil(math.sqrt(meme_num / 16))
    rows = math.ceil(meme_num / cols)

    col_images: list[BuildImage] = []
    for col in range(cols):
        col_meme_list = meme_list[col * rows : (col + 1) * rows]
        max_width = max(
            Text2Image.from_text(
                meme_text(col * rows + row, meme), fontsize=FONTSIZE
            ).width
            + (50 if add_category_icon else 0)
            + 20
            + len(properties.labels) * 35
            for row, (meme, properties) in enumerate(col_meme_list)
        )
        col_image = BuildImage.new("RGBA", (max_width, rows * BLOCK_HEIGHT), BG_COLOR)
        for row, (meme, properties) in enumerate(col_meme_list):
            text = meme_text(col * rows + row, meme)
            block_color = BLOCK_COLOR_1 if (row + col) % 2 == 0 else BLOCK_COLOR_2
            category = "text" if meme.params_type.max_images == 0 else "image"
            col_image.paste(
                text_block(text, max_width, block_color, properties, category),
                (0, row * BLOCK_HEIGHT),
            )
        col_images.append(col_image)

    margin = 30
    frame = BuildImage.new(
        "RGBA",
        (
            sum(image.width for image in col_images) + margin * 2,
            rows * BLOCK_HEIGHT + margin * 2,
        ),
        BG_COLOR,
    )
    x = margin
    y = margin
    for image in col_images:
        frame.paste(image, (x, y))
        x += image.width
    return frame.save_png()
