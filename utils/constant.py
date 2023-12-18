# coding: utf-8
import uuid

from typing import Any
from pydantic import BaseModel, Field, validator
from utils.errs import UrlInvalidSchemaErr


class SpiderPayload(BaseModel):
    uid: str = Field(default_factory=lambda: uuid.uuid4().hex)
    typ: list = []
    ctx: dict = {}
    url: str
    callback: str = ""
    priority: int = 0

    @validator('url')
    def validate_url_http(cls, v):
        if not v:
            return v
        if not isinstance(v, str):
            raise ValueError("Invalid String Type")
        if not v.startswith(("http://", "https://")):
            raise UrlInvalidSchemaErr("请求url不合法")
        return v

    @validator('callback')
    def validate_callback_http(cls, v):
        if not v:
            return v
        if not isinstance(v, str):
            raise ValueError("Invalid String Type")
        if not v.startswith(("http://", "https://")):
            raise UrlInvalidSchemaErr("请求callback不合法")
        return v


class HttpResponse(BaseModel):
    uid: str = None
    code: int = 0
    cost: int = 0
    message: str = "ok"
    data: Any = None
    ctx: dict = {}
