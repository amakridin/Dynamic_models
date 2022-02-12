from pydantic import BaseModel, Field
from typing import Literal


class Pong(BaseModel):
    result: str = Field(default="pong", title="ping result",)


class CheckModel(BaseModel):
    model_name: str
    result: bool


class ModelsList(BaseModel):
    models: list


class Params(BaseModel):
    name: str
    type: Literal["str", "int"]
    nullable: bool


class ModelParams(BaseModel):
    name: str
    params: list[Params]
