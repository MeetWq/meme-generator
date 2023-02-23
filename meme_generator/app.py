import filetype
from typing import List, Optional
from pydantic import ValidationError
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, UploadFile, HTTPException, Response, status, Form, Depends

from meme_generator.manager import get_memes
from meme_generator.config import meme_config
from meme_generator.meme import Meme, MemeArgsModel
from meme_generator.exception import MemeGeneratorException


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
            result = await meme(images=imgs, texts=texts, args=args.dict())
        except MemeGeneratorException as e:
            raise HTTPException(status_code=500, detail=str(e))

        content = result.getvalue()
        media_type = str(filetype.guess_mime(content)) or "text/plain"
        return Response(content=content, media_type=media_type)


def register_routers():
    for meme in get_memes():
        register_router(meme)


def run_server():
    import uvicorn

    register_routers()
    uvicorn.run(app, host=meme_config.server.host, port=meme_config.server.port)


if __name__ == "__main__":
    run_server()
