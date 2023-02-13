import asyncio
import filetype
from functools import partial
from typing import List, Optional
from pydantic import ValidationError
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, UploadFile, HTTPException, Response, status, Form, Depends

from .meme import Meme, MemeArgsModel
from .exception import MemeGeneratorException

app = FastAPI()


def register_router(meme: Meme):

    if args_type := meme.params_type.args_type:
        args_model = args_type.model
    else:
        args_model = MemeArgsModel

    def args_checker(args: Optional[str] = Form(default=str(args_model().json()))):
        if not args:
            return MemeArgsModel()
        try:
            model = args_model.parse_raw(args)
        except ValidationError as e:
            raise HTTPException(
                detail=jsonable_encoder(e.errors()),
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        return model

    @app.post(f"/memes/{meme.key}/")
    async def _(
        images: List[UploadFile] = [],
        texts: List[str] = meme.params_type.default_texts,
        args: args_model = Depends(args_checker),  # type: ignore
    ):
        imgs: List[bytes] = []
        for image in images:
            imgs.append(await image.read())

        texts = [text for text in texts if text]

        assert isinstance(args, args_model)

        try:
            loop = asyncio.get_running_loop()
            pfunc = partial(meme, images=imgs, texts=texts, args=args.dict())
            result = await loop.run_in_executor(None, pfunc)
        except MemeGeneratorException as e:
            raise HTTPException(status_code=500, detail=str(e))

        content = result.getvalue()
        media_type = str(filetype.guess_mime(content)) or "text/plain"
        return Response(content=content, media_type=media_type)
