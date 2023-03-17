from typing import Any, Dict, List, Optional

import filetype
from fastapi import Depends, FastAPI, Form, HTTPException, Response, UploadFile, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ValidationError

from meme_generator.config import meme_config
from meme_generator.exception import MemeGeneratorException, NoSuchMeme
from meme_generator.manager import get_meme, get_meme_keys, get_memes
from meme_generator.meme import Meme, MemeArgsModel

app = FastAPI()


class MemeArgsResponse(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    default: Optional[Any] = None
    enum: Optional[List[Any]] = None


class MemeParamsResponse(BaseModel):
    min_images: int
    max_images: int
    min_texts: int
    max_texts: int
    default_texts: List[str]
    args: List[MemeArgsResponse]


class MemeInfoResponse(BaseModel):
    key: str
    keywords: List[str]
    patterns: List[str]
    params: MemeParamsResponse


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
    @app.get(f"/memes/keys")
    def _():
        return get_meme_keys()

    @app.get("/memes/{key}/info")
    def _(key: str):
        try:
            meme = get_meme(key)
        except NoSuchMeme as e:
            raise HTTPException(status_code=500, detail=str(e))

        args_model = (
            meme.params_type.args_type.model
            if meme.params_type.args_type
            else MemeArgsModel
        )
        properties: Dict[str, Dict[str, Any]] = args_model.schema().get(
            "properties", {}
        )
        properties.pop("user_infos")
        return MemeInfoResponse(
            key=meme.key,
            keywords=meme.keywords,
            patterns=meme.patterns,
            params=MemeParamsResponse(
                min_images=meme.params_type.min_images,
                max_images=meme.params_type.max_images,
                min_texts=meme.params_type.min_texts,
                max_texts=meme.params_type.max_texts,
                default_texts=meme.params_type.default_texts,
                args=[
                    MemeArgsResponse(
                        name=name,
                        type=info.get("type", ""),
                        description=info.get("description"),
                        default=info.get("default"),
                        enum=info.get("enum"),
                    )
                    for name, info in properties.items()
                ],
            ),
        )

    @app.get("/memes/{key}/preview")
    async def _(key: str):
        try:
            meme = get_meme(key)
            result = await meme.generate_preview()
        except MemeGeneratorException as e:
            raise HTTPException(status_code=500, detail=str(e))

        content = result.getvalue()
        media_type = str(filetype.guess_mime(content)) or "text/plain"
        return Response(content=content, media_type=media_type)

    @app.post("/memes/{key}/parse_args")
    async def _(key: str, args: List[str] = []):
        try:
            meme = get_meme(key)
            return meme.parse_args(args)
        except MemeGeneratorException as e:
            raise HTTPException(status_code=500, detail=str(e))

    for meme in sorted(get_memes(), key=lambda meme: meme.key):
        register_router(meme)


def run_server():
    import uvicorn

    register_routers()
    uvicorn.run(app, host=meme_config.server.host, port=meme_config.server.port)


if __name__ == "__main__":
    run_server()
