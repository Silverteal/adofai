# ADOFAI

*和 A Dance Of Fire And Ice （中文名“冰与火之舞”）没有任何关系*

ADOFAI (Adjustable Data Objects For Authlib Injector) 是一组数据模型和配套工具，旨在简化自定义实现 Authlib-injector 的规范
Yggdrasil 服务端、客户端及其配套程序的过程。

## 快速开始

```python
from adofai import GameName, GameProfile, TextureProfile, TextureProperty, TextureUrl
from adofai.utils.uuid import offline_uuid
from adofai.utils.signing import dummy_key

texture = TextureProfile(
    skin=TextureProperty(
        url=TextureUrl("https://something"),
        metadata={"model": "slim"}
    ),
    cape=TextureProperty(
        url=TextureUrl("https://yetanother")
    )
)

game_profile = GameProfile(
    name="Notch",
    id=offline_uuid(GameName("Notch")),
    texture=texture,
    extra_properties={"uploadableTextures": "skin,cape"}
)

print(game_profile.serialize("full", dummy_key()))

```