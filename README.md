# layered-config-py

* 複数の設定を読み込むことが出来る
* 後に読み込まれた設定は、前に読み込まれた設定に上書きマージする
* 設定はTOMLファイルへのパス、もしくは`dict`オブジェクトで指定出来る
* 読み込まれた設定は読み取り専用、かつattribute参照可能な`dict`で返される

```py
from layered_config import LayeredConfig

DEFAULT_CONFIG = {"main": {"debug": False}}

config = LayeredConfig.load(DEFAULT_CONFIG, "~/.app/config.toml", "./.app/config.toml")

print(config.main.debug)
```
