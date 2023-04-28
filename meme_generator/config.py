import json
from pathlib import Path
from typing import List, Optional, Union

import toml
from pydantic import BaseModel, Extra

from .dirs import get_config_file

config_file_path = get_config_file("config.toml")


class MemeConfig(BaseModel):
    load_builtin_memes: bool = True
    meme_dirs: List[Path] = []
    meme_disabled_list: List[str] = []


class ResourceConfig(BaseModel):
    resource_url: Optional[str] = None
    resource_urls: List[str] = [
        "https://raw.githubusercontent.com/MeetWq/meme-generator/",
        "https://ghproxy.com/https://raw.githubusercontent.com/MeetWq/meme-generator/",
        "https://fastly.jsdelivr.net/gh/MeetWq/meme-generator@",
        "https://raw.fastgit.org/MeetWq/meme-generator/",
        "https://raw.fgit.ml/MeetWq/meme-generator/",
        "https://raw.gitmirror.com/MeetWq/meme-generator/",
        "https://raw.kgithub.com/MeetWq/meme-generator/",
    ]


class GifConfig(BaseModel):
    gif_max_size: float = 10
    gif_max_frames: int = 100


class TranslatorConfig(BaseModel):
    baidu_trans_appid: str = ""
    baidu_trans_apikey: str = ""


class ServerConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 2233


class LogConfig(BaseModel):
    log_level: Union[int, str] = "INFO"


class Config(BaseModel, extra=Extra.ignore):
    meme: MemeConfig = MemeConfig()
    resource: ResourceConfig = ResourceConfig()
    gif: GifConfig = GifConfig()
    translate: TranslatorConfig = TranslatorConfig()
    server: ServerConfig = ServerConfig()
    log: LogConfig = LogConfig()

    @classmethod
    def load(cls) -> "Config":
        return cls.parse_obj(toml.load(config_file_path))

    def dump(self):
        with open(config_file_path, "w", encoding="utf8") as f:
            toml.dump(json.loads(self.json()), f)


if not config_file_path.exists():
    meme_config = Config()
    config_file_path.write_text("", encoding="utf8")
else:
    meme_config = Config.load()
