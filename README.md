<div align="center">

<img src="https://s2.loli.net/2023/03/26/4URd1BKj3ToycLl.png" width=200 />

# meme-generator

_✨ 表情包生成器，用于制作各种沙雕表情包 ✨_

<p align="center">
  <img src="https://img.shields.io/github/license/MeetWq/meme-generator" alt="license">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python">
  <a href="https://pypi.org/project/meme-generator">
    <img src="https://badgen.net/pypi/v/meme-generator" alt="pypi">
  </a>
  <a href="https://jq.qq.com/?_wv=1027&k=wDVNrMdr">
    <img src="https://img.shields.io/badge/QQ%E7%BE%A4-682145034-orange" alt="qq group">
  </a>
</p>

</div>


> **Note**
>
> 额外表情仓库：[meme-generator-contrib](https://github.com/MeetWq/meme-generator-contrib)


## 表情列表

表情详细信息、表情预览等可以在 [--> 表情列表 <--](docs/memes.md) 查看


## 安装

### 本地安装

本地安装、图片下载、字体安装方式等可以在 [--> 本地安装 <--](docs/install.md) 查看

### Docker

Docker 部署方式可以在 [--> Docker部署 <--](docs/docker.md) 查看


## 使用

### 通过 python 程序调用

参考 [docs/examples/test_meme.py](https://github.com/MeetWq/meme-generator/tree/main/docs/examples/test_meme.py)


### 通过命令行使用

```bash
meme -h/--help
```
- `meme list (ls)` 列出所有已加载的表情
- `meme info (show) KEY` 查看某个表情的详细信息，如：`meme info petpet`
- `meme preview KEY` 使用默认（随机）参数生成预览结果，如：`meme preview petpet`
- `meme generate (make) KEY --text TEXTS --images IMAGES ...` 制作表情，如：`meme generate petpet --images avatar.jpg`

    部分表情有额外的参数，可通过 `-h/--help` 查看，如：`meme generate petpet --help`
- `meme run (start)` 启动 web server，可通过 api 方式调用
- `meme download` 下载内置的表情包所需的图片

### 通过 api 方式使用

执行 `meme run` 可以启动 web 服务器

web 框架用的是 FastApi , 可查看自动生成的交互式 API 文档（访问 http://127.0.0.1:2233/docs ）

可以调用 api 接口使用，python 调用方式可参考 [docs/examples/test_api.py](https://github.com/MeetWq/meme-generator/tree/main/docs/examples/test_api.py)

### 接入聊天机器人使用

- NoneBot
  - [noneplugin/nonebot-plugin-memes](https://github.com/noneplugin/nonebot-plugin-memes) Nonebot2 表情包制作插件
  - [noneplugin/nonebot-plugin-memes-api](https://github.com/noneplugin/nonebot-plugin-memes-api) nonebot-plugin-memes 调用 api 版本
- Yunzai
  - [ikechan8370/yunzai-meme](https://github.com/ikechan8370/yunzai-meme) Yunzai机器人的表情包插件
- Koishi
  - [lgc2333/koishi-plugin-memes-api](https://github.com/lgc2333/koishi-plugin-memes-api) Koishi 复刻版 表情包制作插件调用 API 版


## 配置

默认配置文件位置：

- Windows: `C:\Users\<username>\AppData\Roaming\meme_generator\config.toml`
- Linux: `~/.config/meme_generator/config.toml`
- Mac: `~/Library/Application Support/meme_generator/config.toml`

> **Warning**
>
> 从 v0.0.6 版本开始，不再生成默认配置文件；修改配置时需在对应的文件位置自行创建配置文件
>
> 由于 v0.0.6 版本更改了资源链接的拼接方式，如果装过之前的版本，需要修改配置中的 `resource_url`
>
> **建议将配置文件中不需要更改的选项删除，以使用默认配置**

默认配置：
```toml
[meme]
load_builtin_memes = true  # 是否加载内置表情包
meme_dirs = []  # 加载其他位置的表情包，填写文件夹路径
meme_disabled_list = []  # 禁用的表情包列表，填写表情的 `key`

[resource]
# 下载内置表情包图片时的资源链接，下载时选择最快的站点
resource_urls = [
  "https://raw.githubusercontent.com/MeetWq/meme-generator/",
  "https://ghproxy.com/https://raw.githubusercontent.com/MeetWq/meme-generator/",
  "https://fastly.jsdelivr.net/gh/MeetWq/meme-generator@",
  "https://raw.fastgit.org/MeetWq/meme-generator/",
  "https://raw.fgit.ml/MeetWq/meme-generator/",
  "https://raw.gitmirror.com/MeetWq/meme-generator/",
  "https://raw.kgithub.com/MeetWq/meme-generator/",
]

[gif]
gif_max_size = 10.0  # 限制生成的 gif 文件大小，单位为 Mb
gif_max_frames = 100  # 限制生成的 gif 文件帧数

[translate]
baidu_trans_appid = ""  # 百度翻译api相关，表情包 `dianzhongdian` 需要使用
baidu_trans_apikey = ""  # 可在 百度翻译开放平台 (http://api.fanyi.baidu.com) 申请

[server]
host = "127.0.0.1"  # web server 监听地址
port = 2233  # web server 端口

[log]
log_level = "INFO"  # 日志等级
```


## 加载其他表情

如果希望加载非本仓库内置的表情，可以在 [配置文件](#配置) 中填写表情所在的文件夹路径

如以下的文件夹：

```
/path/to/your/meme_dir
└── meme1
    └── __init__.py
└── meme2
    └── __init__.py
```

在配置文件中修改 `meme_dirs` 如下：

```toml
[meme]
meme_dirs = ["/path/to/your/meme_dir"]
```


## 开发

如果希望编写、贡献新的表情，可以参考 [--> 新表情编写指北 <--](docs/develop.md)

对于一些不适合放在主仓库的表情，可以提交至 [额外表情仓库](https://github.com/MeetWq/meme-generator-contrib)


## 声明

本仓库的表情素材等均来自网络，如有侵权请联系作者删除


## 鸣谢

本仓库的表情整合自原 [nonebot-plugin-petpet](https://github.com/noneplugin/nonebot-plugin-petpet) 和 [nonebot-plugin-memes](https://github.com/noneplugin/nonebot-plugin-memes) 仓库

感谢以下开发者作出的贡献：

<a href="https://github.com/noneplugin/nonebot-plugin-petpet/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=noneplugin/nonebot-plugin-petpet&max=1000" />
</a>


部分表情素材或代码参考了以下项目，感谢这些项目的开发者们

- [Ailitonia/omega-miya](https://github.com/Ailitonia/omega-miya) 基于nonebot2的qq机器人
- [FloatTech/ZeroBot-Plugin](https://github.com/FloatTech/ZeroBot-Plugin) 基于 ZeroBot 的 OneBot 插件
- [HibiKier/zhenxun_bot](https://github.com/HibiKier/zhenxun_bot) 基于 Nonebot2 和 go-cqhttp 开发，以 postgresql 作为数据库，非常可爱的绪山真寻bot
- [SAGIRI-kawaii/sagiri-bot](https://github.com/SAGIRI-kawaii/sagiri-bot) 基于Graia Ariadne和Mirai的QQ机器人 SAGIRI-BOT
- [Dituon/petpet](https://github.com/Dituon/petpet) Mirai插件 生成各种奇怪的图片
- [kexue-z/nonebot-plugin-nokia](https://github.com/kexue-z/nonebot-plugin-nokia) 诺基亚手机图生成
- [RafuiiChan/nonebot_plugin_charpic](https://github.com/RafuiiChan/nonebot_plugin_charpic) 字符画生成插件
