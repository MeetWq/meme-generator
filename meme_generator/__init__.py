from pathlib import Path

from meme_generator.meme import Meme as Meme
from meme_generator.meme import MemeArgsType as MemeArgsType
from meme_generator.meme import MemeArgsModel as MemeArgsModel
from meme_generator.meme import MemeParamsType as MemeParamsType

from meme_generator.manager import add_meme as add_meme
from meme_generator.manager import get_meme as get_meme
from meme_generator.manager import load_memes as load_memes
from meme_generator.manager import get_meme_keys as get_meme_keys

from meme_generator.config import meme_config as config

from meme_generator.version import __version__

load_memes(Path(__file__).parent / "memes")
for meme_dir in config.meme.meme_dirs:
    load_memes(meme_dir)
