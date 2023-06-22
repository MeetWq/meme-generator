## 本地安装

### 使用 pip 安装

```bash
pip install meme_generator
```

#### 图片下载

由于表情包图片体积较大，`meme-generator` 包含的表情中的图片并不随代码一起打包，需要在安装后手动执行下载命令：

```bash
meme download
```

### 直接运行源代码

克隆当前仓库：

```bash
git clone https://github.com/MeetWq/meme-generator
```

通过 `python -m meme_generator.app` 运行 web 服务器

通过 `python -m meme_generator.cli` 运行命令行程序


### 字体安装

为确保表情包中的文字生成正常，需要自行安装字体

> **Note**
>
> 字体安装后若文字仍显示不正常，可删掉 `matplotlib` 字体缓存文件重新运行程序
>
> 缓存文件位置：
> - Windows: `C:\Users\<username>\.matplotlib\fontlist-xxx.json`
> - Linux: `~/.cache/matplotlib/fontlist-xxx.json`
> - Mac: `~/Library/Caches/matplotlib/fontlist-xxx.json`


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
| [FZKaTong-M19S](https://www.foundertype.com/index.php/FontInfo/index/id/136) | [FZKATJW.ttf](https://github.com/MeetWq/meme-generator/blob/main/resources/fonts/FZKATJW.ttf) | `capoo_say` | 方正卡通 |
| [FZXS14](https://www.foundertype.com/index.php/FontInfo/index/id/208) | [FZXS14.ttf](https://github.com/MeetWq/meme-generator/blob/main/resources/fonts/FZXS14.ttf) | `nokia` | 方正像素14 |
| [FZSJ-QINGCRJ](https://www.foundertype.com/index.php/FontInfo/index/id/5178) | [FZSJ-QINGCRJ.ttf](https://github.com/MeetWq/meme-generator/blob/main/resources/fonts/FZSJ-QINGCRJ.ttf) | `psyduck`、`nijika_holdsign` | 方正手迹-青春日记 |
| [FZShaoEr-M11S](https://www.foundertype.com/index.php/FontInfo/index/id/149) | [FZSEJW.ttf](https://github.com/MeetWq/meme-generator/blob/main/resources/fonts/FZSEJW.ttf) | `raise_sign`、`nekoha_holdsign` | 方正少儿 |
| [NotoSansSC](https://fonts.google.com/noto/specimen/Noto+Sans+SC) | [NotoSansSC-Regular.otf](https://github.com/MeetWq/meme-generator/blob/main/resources/fonts/NotoSansSC-Regular.otf) | `5000choyen` |  |
| [NotoSerifSC](https://fonts.google.com/noto/specimen/Noto+Serif+SC) | [NotoSerifSC-Regular.otf](https://github.com/MeetWq/meme-generator/blob/main/resources/fonts/NotoSerifSC-Regular.otf) | `5000choyen` |  |
| [HiraginoMin](https://www.fonts.net.cn/font-36201269101.html) | [HiraginoMin-W5-90-RKSJ-H-2.ttc](https://github.com/MeetWq/meme-generator/blob/main/resources/fonts/HiraginoMin-W5-90-RKSJ-H-2.ttc) | `oshi_no_ko` | 明朝体 |


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
