from functools import wraps
from typing import List, Set, Optional, Iterable

from .models import Meme, MemeFunction, MemeParamsType, MemeArgsType


class MemeManager:
    def __init__(
        self,
        memes: Optional[Iterable[Meme]] = None,
    ) -> None:
        self.memes: Set[Meme] = set(memes or [])


meme_manager = MemeManager()


def new_meme(
    key: str,
    keywords: List[str],
    *,
    min_images: int = 0,
    max_images: int = 0,
    min_texts: int = 0,
    max_texts: int = 0,
    args_type: Optional[MemeArgsType] = None
):
    def decorator(func: MemeFunction):
        @wraps(func)
        def wrapper(*args, **kwargs):
            meme = Meme(
                key,
                keywords,
                func,
                MemeParamsType(min_images, max_images, min_texts, max_texts, args_type),
            )
            meme_manager.memes.add(meme)

            return func(*args, **kwargs)

        return wrapper

    return decorator
