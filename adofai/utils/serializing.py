# coding=utf-8
"""序列化，解析属性等的工具"""
__all__ = []

from typing import Iterable, Literal, Mapping

from adofai import ProfileProperties

def parse_property(v: Iterable[Mapping[Literal["name"] | Literal["value"], str]]) -> ProfileProperties:
    """
    将形如

    ``[{"name":"preferredLanguage","value":"zh_CN"}]``

    的列表/可迭代对象（常见于 Yggdrasil API 响应结果）解析为形如

    ``{"preferredLanguage":"zh_CN"}``

    的简化格式，用于构造函数。
    """
# todo remove this
if __name__ == "__main__":
    from pydantic import BaseModel, model_serializer


class Model(BaseModel):
    x: str

    @model_serializer
    def ser_model(self) -> str:
        return self.x


print(Model(x='not a dict').model_dump_json())
