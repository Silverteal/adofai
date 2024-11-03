# coding=utf-8
from typing import Literal, Optional, overload
from uuid import uuid4

from Crypto.PublicKey.RSA import RsaKey
from pydantic import BaseModel, field_serializer

from adofai import GameId, GameName, ProfileProperties, SerializedProfile, TextureUrl, UserId
from adofai.utils.signing import sign_property
from adofai.utils.uuids import uuid_to_str


class Texture(BaseModel):
    """单个材质属性，注意属性名称是小写的"""

    url: TextureUrl
    metadata: dict[str, str] | None = None


class GameProfile(BaseModel):
    id: GameId
    name: GameName
    texture: dict[str, Texture] = {}
    extra_properties: ProfileProperties = {}


    @overload
    def serialize(self, export_level: Literal["unsigned", "minimum"]) -> SerializedProfile:
        """不需要签名的序列化无须提供私钥"""

    @overload
    def serialize(self, export_level: Literal["full"], key: RsaKey) -> SerializedProfile:
        """需要签名的序列化必须提供私钥"""

    def serialize(self, export_level: Literal["full", "unsigned", "minimum"],
                  key: Optional[RsaKey] = None) -> SerializedProfile:
        """导出游戏角色档案为需要的格式。todo"""
        structure = {
            "id": uuid_to_str(self.id),
            "name": self.name,
        }

        if export_level == "minimum":
            return structure

        structure["properties"] = []

        if self.texture:
            structure["properties"] += [
                {
                    "name": "textures",
                    "value": self.texture.serialize(id=self.id, name=self.name),
                }
            ]

        structure["properties"] += [
            {
                "name": k,
                "value": v,
            }
            for k, v in self.extra_properties.items()
        ]

        if export_level == "unsigned":
            return structure

        for token in structure["properties"]:
            # 迭代出的是否是引用？赋值是否有效？
            token["signature"] = sign_property(token["value"], key)

        return structure


class UserProfile(BaseModel):
    id: UserId
    properties: ProfileProperties = {}

    @field_serializer("id")
    def serialize_id(self, id: UserId) -> str:
        """UUID 转换为为无符号 UUID 文本"""
        return uuid_to_str(id)

    @field_serializer("properties")
    def serialize_properties(self, properties: ProfileProperties) -> list[ProfileProperties]:
        """字典转换为列表"""
        return [{"name": k, "value": v} for k, v in properties.items()]


if __name__ == "__main__":
    a = GameProfile(id=GameId(uuid4()), name=GameName("player"), texture={"skin": Texture(url=TextureUrl("skin.png"))})
    print(a)
    print(repr(a.texture))
    print(a.texture["SkIn"])
