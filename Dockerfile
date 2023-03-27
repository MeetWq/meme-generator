FROM python:3.10 as tmp

WORKDIR /tmp

ENV PATH="${PATH}:/root/.local/bin"

COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN pip install poetry \
  && poetry config virtualenvs.in-project true \
  && poetry install --no-dev --no-interaction --no-ansi

FROM python:3.10-slim as app

WORKDIR /app

ENV TZ=Asia/Shanghai \
  LANG=zh_CN.UTF-8 \
  LC_ALL=zh_CN.UTF-8 \
  PATH="/app/.venv/bin:${PATH}" \
  VIRTUAL_ENV="/app/.venv" \
  PYTHONPATH=/app \
  LOAD_BUILTIN_MEMES=true \
  MEME_DIRS="[\"/data/memes\"]" \
  MEME_DISABLED_LIST="[]" \
  GIF_MAX_SIZE=10.0 \
  GIF_MAX_FRAMES=100 \
  BAIDU_TRANS_APPID="" \
  BAIDU_TRANS_APIKEY=""

EXPOSE 2233

VOLUME /data

COPY meme_generator /app/meme_generator
COPY --from=tmp /tmp/.venv /app/.venv
COPY resources/fonts/* /usr/share/fonts/meme-fonts/
RUN apt-get update \
  && apt-get install -y locales fontconfig fonts-noto-cjk fonts-noto-color-emoji \
  && apt-get clean \
  && locale-gen zh_CN zh_CN.UTF-8 \
  && fc-cache -fv \
  && mkdir -p /data/memes \
  && mkdir -p ~/.config/meme_generator \
  && echo "\
[meme]\n\
load_builtin_memes = $LOAD_BUILTIN_MEMES\n\
meme_dirs = $MEME_DIRS\n\
meme_disabled_list = $MEME_DISABLED_LIST\n\
[gif]\n\
gif_max_size = $GIF_MAX_SIZE\n\
gif_max_frames = $GIF_MAX_FRAMES\n\
[translate]\n\
baidu_trans_appid = \"$BAIDU_TRANS_APPID\"\n\
baidu_trans_apikey = \"$BAIDU_TRANS_APIKEY\"\n\
[server]\n\
host = \"0.0.0.0\"\n\
port = 2233\n\
" >> ~/.config/meme_generator/config.toml

CMD ["python", "meme_generator/app.py"]
