<div align="center">

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


## 安装

使用 pip 安装

```bash
pip install meme_generator
```


### 图片下载

由于表情包图片体积较大，`meme-generator` 包含的表情中的图片并不随代码一起打包，需要在安装后手动执行下载命令：

```
meme download
```

也可以调用 `meme_generator/download.py` 中的 `check_resources` 函数进行下载


### 字体安装

为确保表情包中的文字生成正常，需要自行安装字体

#### 中文字体 和 emoji字体 安装

根据系统的不同，推荐安装的字体如下：

- Windows:

大部分 Windows 系统自带 [微软雅黑](https://learn.microsoft.com/zh-cn/typography/font-list/microsoft-yahei) 中文字体 和 [Segoe UI Emoji](https://learn.microsoft.com/zh-cn/typography/font-list/segoe-ui-emoji) emoji 字体，一般情况下无需额外安装


- Linux:

部分系统可能自带 [文泉驿微米黑](http://wenq.org/wqy2/index.cgi?MicroHei) 中文字体；

对于 Ubuntu 系统，推荐安装 Noto Sans CJK 和 Noto Color Emoji：

```bash
sudo apt install fonts-noto-cjk fonts-noto-color-emoji
```

为避免 Noto Sans CJK 中部分中文显示为异体（日文）字形，可以将简体中文设置为默认语言（详见 [ArchWiki](https://wiki.archlinux.org/title/Localization/Simplified_Chinese?rdfrom=https%3A%2F%2Fwiki.archlinux.org%2Findex.php%3Ftitle%3DLocalization_%28%25E7%25AE%2580%25E4%25BD%2593%25E4%25B8%25AD%25E6%2596%2587%29%2FSimplified_Chinese_%28%25E7%25AE%2580%25E4%25BD%2593%25E4%25B8%25AD%25E6%2596%2587%29%26redirect%3Dno#%E4%BF%AE%E6%AD%A3%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87%E6%98%BE%E7%A4%BA%E4%B8%BA%E5%BC%82%E4%BD%93%EF%BC%88%E6%97%A5%E6%96%87%EF%BC%89%E5%AD%97%E5%BD%A2)）：

```bash
sudo locale-gen zh_CN zh_CN.UTF-8
sudo update-locale LC_ALL=zh_CN.UTF-8 LANG=zh_CN.UTF-8
fc-cache -fv
```

其他 Linux 系统可以自行下载字体文件安装：

思源黑体：https://github.com/adobe-fonts/source-han-sans

NotoSansSC：https://fonts.google.com/noto/specimen/Noto+Sans+SC

Noto Color Emoji：https://github.com/googlefonts/noto-emoji


- Mac:

苹果系统一般自带 "PingFang SC" 中文字体 与 "Apple Color Emoji" emoji 字体


#### 其他字体安装

某些表情包需要用到一些额外字体，存放于仓库中 [resources/fonts](https://github.com/MeetWq/meme-generator/tree/main/resources/fonts)，需要自行下载安装

具体字体及对应的表情如下：

| 字体名 | 字体文件名 | 用到该字体的表情 | 备注 |
| --- | --- | --- | --- |
| [Consolas](https://learn.microsoft.com/zh-cn/typography/font-list/consolas) | [consola.ttf](https://github.com/MeetWq/meme-generator/blob/main/resources/fonts/consola.ttf) | `charpic` |  |
| [方正像素14](https://www.foundertype.com/index.php/FontInfo/index/id/208) | [FZXS14.ttf](https://github.com/MeetWq/meme-generator/blob/main/resources/fonts/FZXS14.ttf) | `nokia` | 像素体 |
| [方正手迹-青春日记](https://www.foundertype.com/index.php/FontInfo/index/id/5178) | [FZSJ-QINGCRJ.ttf](https://github.com/MeetWq/meme-generator/blob/main/resources/fonts/FZSJ-QINGCRJ.ttf) | `psyduck` | 手写体 |
| [方正少儿](https://www.foundertype.com/index.php/FontInfo/index/id/149) | [FZSEJW.ttf](https://github.com/MeetWq/meme-generator/blob/main/resources/fonts/FZSEJW.ttf) | `raise_sign` | 少儿体 |
| [NotoSansSC](https://fonts.google.com/noto/specimen/Noto+Sans+SC) | [NotoSansSC-Regular.otf](https://github.com/MeetWq/meme-generator/blob/main/resources/fonts/NotoSansSC-Regular.otf) | `5000choyen` |  |
| [NotoSerifSC](https://fonts.google.com/noto/specimen/Noto+Serif+SC) | [NotoSerifSC-Regular.otf](https://github.com/MeetWq/meme-generator/blob/main/resources/fonts/NotoSerifSC-Regular.otf) | `5000choyen` |  |


#### 字体安装方式

不同系统的字体安装方式：

- Windows:
    - 双击通过字体查看器安装
    - 复制到字体文件夹：`C:\Windows\Fonts`

- Linux:

在 `/usr/share/fonts` 目录下新建文件夹，如 `myfonts`，将字体文件复制到该路径下；

运行如下命令建立字体缓存：

```bash
fc-cache -fv
```

- Mac:

使用字体册打开字体文件安装


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
- `meme generate (make) KEY -t/--text TEXTS -i/--images IMAGES ...` 制作表情，如：`meme generate petpet -i avatar.jpg`

    部分表情有额外的参数，可通过 `-h/--help` 查看，如：`meme generate petpet --help`
- `meme run (start)` 启动 web server，可通过 api 方式调用
- `meme download` 下载内置的表情包所需的图片

### 通过 api 方式使用

执行 `meme run` 可以启动 web 服务器

web 框架用的是 FastApi , 可查看自动生成的交互式 API 文档（访问 http://127.0.0.1:2233/docs ）

可以调用 api 接口使用，python 调用方式可参考 [docs/examples/test_api.py](https://github.com/MeetWq/meme-generator/tree/main/docs/examples/test_api.py)


## 配置

默认配置文件位置：

- Windows: `C:\Users\<username>\AppData\Local\meme_generator\config.toml`
- Linux: `~/.config/meme_generator/config.toml`
- Mac: `~/Library/Application Support/meme_generator/config.toml`

默认配置：
```toml
[meme]
load_builtin_memes = true  # 是否加载内置表情包
meme_dirs = []  # 加载其他位置的表情包，填写文件夹路径
meme_disabled_list = []  # 禁用的表情包列表，填写表情的 `key`

[resource]
resource_url = "https://ghproxy.com/https://github.com/MeetWq/meme-generator"  # 下载内置表情包图片时的资源链接

[gif]
gif_max_size = 10.0  # 限制生成的 gif 文件大小，单位为 Mb
gif_max_frames = 100  # 限制生成的 gif 文件帧数

[translate]
baidu_trans_appid = ""  # 百度翻译api相关，表情包 `dianzhongdian` 需要使用
baidu_trans_apikey = ""  # 可在 百度翻译开放平台 (http://api.fanyi.baidu.com) 申请

[server]
host = "127.0.0.1"  # web server 监听地址
port = 2233  # web server 端口
```


## 开发

### 加载其他表情

TODO


## TODO

- [ ] 生成表情列表及预览
- [ ] 加载其他表情的示例
