from pathlib import Path

from layered_config.layered_config import LayeredConfig


class TestLayeredConfig:
    def test_load__from_files(self, tmp_path: Path):
        path1 = tmp_path / "a.toml"
        with path1.open(mode="wt") as f:
            f.write("[Default]\n")
            f.write("a = 'alpha'\n")

        path2 = tmp_path / "b.toml"
        with path2.open(mode="wt") as f:
            f.write("[Default]\n")
            f.write("b = 'bravo'\n")

        config = LayeredConfig.load(path1, path2)

        assert config == {"Default": {"a": "alpha", "b": "bravo"}}
        assert config.Default.a == "alpha"
        assert config.Default.b == "bravo"

    def test_load__with_dict(self, tmp_path: Path):
        default = {"main": {"a": 1, "b": 2}}

        path = tmp_path / "a.toml"
        with path.open(mode="wt") as f:
            f.write("[main]\n")
            f.write("a = 'alpha'\n")

        config = LayeredConfig.load(default, path)

        assert config == {"main": {"a": "alpha", "b": 2}}

    def test_load__no_such_files(self, tmp_path: Path):
        path1 = tmp_path / "a.toml"
        path2 = tmp_path / "b.toml"

        config = LayeredConfig.load(path1, path2)

        assert config == {}
