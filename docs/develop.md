# 新表情编写指北

## 表情注册

meme-generator 会以包的形式加载表情，通过 `add_meme` 函数来“注册”一个表情

以 `petpet` 表情为例，文件结构如下：

```
meme_generator/memes/petpet
├── __init__.py  # 表情制作程序
└── images  # 表情需要的图片文件
    ├── 0.png
    ├── 1.png
    ├── 2.png
    ├── 3.png
    └── 4.png
```

在不考虑额外参数的情况下，`petpet` 表情的 `__init__.py` 编写如下：

```python
from typing import List
from pathlib import Path
from pil_utils import BuildImage
from PIL.Image import Image as IMG

from meme_generator.utils import save_gif
from meme_generator import add_meme


img_dir = Path(__file__).parent / "images"


def petpet(images: List[BuildImage], texts, args):
    """表情制作函数

    函数会接收 3 个参数：
    - `images`: 传入的图片列表，类型为 `pil_utils.BuildImage`
    - `texts`: 传入的文字列表，类型为 `str`
    - `args`: 其他参数，类型为 `meme_generator.meme.MemeArgsModel`
    """
    img = images[0].convert("RGBA").square()
    frames: List[IMG] = []
    locs = [
        (14, 20, 98, 98),
        (12, 33, 101, 85),
        (8, 40, 110, 76),
        (10, 33, 102, 84),
        (12, 20, 98, 98),
    ]
    for i in range(5):
        hand = BuildImage.open(img_dir / f"{i}.png")
        frame = BuildImage.new("RGBA", hand.size, (255, 255, 255, 0))
        x, y, w, h = locs[i]
        frame.paste(img.resize((w, h)), (x, y), alpha=True)
        frame.paste(hand, alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.06)


add_meme(
    "petpet",  # 表情唯一名
    petpet,  # 表情制作函数
    min_images=1,  # 至少需要 1 张图片
    max_images=1,  # 另有 `min_texts` 和 `max_texts` 选项来控制传入文字的数量
    keywords=["摸", "摸摸", "摸头", "rua"],  # 关键词，填写言简意赅的词语，用于展示表情含义、方便聊天Bot调用等
)
```

通常情况下，建议每个表情一个文件夹，表情所需的图片文件等都放置于该文件夹中，方便增删表情

也可以一个文件中注册多个表情，如：[gif_subtitle](../meme_generator/memes/gif_subtitle/__init__.py)


## 参数定义

部分表情需要额外的参数。表情参数的类型定义如下：

```python
@dataclass
class MemeArgsType:
    parser: ArgumentParser  # 参数解析器，将命令行形式的文本解析为字典形式，方便通过命令行使用
    model: Type[MemeArgsModel]  # 参数模型，用于验证字典形式的参数，并传入表情制作函数
    instances: List[MemeArgsModel] = field(default_factory=list)  # 可选，参数模型示例，推荐填写，方便生成不同参数下的预览图
```

以 `petpet` 表情为例，需要定义一个控制图片是否变为圆形的参数 `circle`

可以定义如下的 `pydantic` 模型：

```python
from pydantic import Field
from meme_generator import MemeArgsModel

class Model(MemeArgsModel):
    circle: bool = Field(False, description="是否将图片变为圆形")
```

定义参数时推荐使用 `Field` 定义默认值，可以定义 `description` 描述参数含义，方便生成文档

同时定义如下的参数解析器：

```python
from argparse import ArgumentParser

parser = ArgumentParser(prefix_chars="-/")
parser.add_argument("--circle", "/圆", action="store_true", help="是否将图片变为圆形")
```

以上参数解析器可以将形如 `["--circle"]` 的参数列表解析为 `{"circle": true}` 的形式，继而通过 `pydantic` 模型验证

推荐在定义选项时添加自然语言风格的别名，如 `/圆`，这样可以方便聊天机器人等场合调用，比如可以解析 `摸头 /圆` 这样的文本

定义好上述的 `parser` 和 `Model` 后，需要在 `add_meme` 时传入：

```python
add_meme(
    "petpet",
    petpet,
    min_images=1,
    max_images=1,
    args_type=MemeArgsType(
        parser,
        Model,
        [
            Model(circle=False),
            Model(circle=True),
        ],
    ),
    keywords=["摸", "摸摸", "摸头", "rua"],
)
```

这里传入了 `circle=False` 和 `circle=True` 两个模型实例，可以在生成文档时生成不同参数时的预览图，效果如 [memes.md](memes.md#petpet) 所示


## 加载表情

如果希望加载非本仓库内置的表情，可以在 [配置文件](../README.md#配置) 中填写表情所在的文件夹路径

如以下的文件夹：

```
/path/to/your/meme_dir
└── new_meme
    └── __init__.py
```

在配置文件中修改 `meme_dirs` 如下：

```toml
[meme]
meme_dirs = ["/path/to/your/meme_dir"]
```
