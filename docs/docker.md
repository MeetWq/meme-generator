https://github.com/MeetWq/meme-generator

## Docker部署

### 运行

```shell
docker run -d \
  --name=meme-generator \
  -p 2233:2233 \
  --restart always \
  meetwq/meme-generator:main
```

运行后可通过 api 方式调用


### 环境变量

| 变量名 | 默认值 | 说明 |
| --- | --- | --- |
| `MEME_DIRS` | `'["/data/memes"]'` | 额外表情路径 |
| `MEME_DISABLED_LIST` | `'[]'` | 禁用表情列表 |
| `GIF_MAX_SIZE` | `10.0` | 限制生成的 gif 文件大小 |
| `GIF_MAX_FRAMES` | `100` | 限制生成的 gif 文件帧数 |
| `BAIDU_TRANS_APPID` | `''` | 百度翻译 appid |
| `BAIDU_TRANS_APIKEY` | `''` | 百度翻译 apikey |


### 加载额外表情

可通过 `MEME_DIRS` 环境变量指定额外表情路径，默认为 `["/data/memes"]`

可将 docker 路径 `/data` 映射到本地路径 `<YOUR_DATA_DIR>`

将额外表情放置于 `<YOUR_DATA_DIR>/memes` 即可


完整的运行示例：

```shell
docker run -d \
  --name=meme-generator \
  -p 2233:2233 \
  --restart always \
  -v <YOUR_DATA_DIR>:/data \
  -e MEME_DIRS='["/data/memes"]' \
  -e MEME_DISABLED_LIST='[]' \
  -e GIF_MAX_SIZE=10.0 \
  -e GIF_MAX_FRAMES=100 \
  -e BAIDU_TRANS_APPID=<YOUR_BAIDU_TRANS_APPID> \
  -e BAIDU_TRANS_APIKEY=<YOUR_BAIDU_TRANS_APIKEY> \
  meetwq/meme-generator:main
```
