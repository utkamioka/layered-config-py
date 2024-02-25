from pathlib import Path

import pytest
from _pytest.monkeypatch import MonkeyPatch

from layered_config.layered_config import LayeredConfig


class TestLayeredConfig:
    @pytest.fixture
    def temp_home_dir(self, tmp_path: Path, monkeypatch: MonkeyPatch) -> Path:
        homedir = tmp_path / "home"
        homedir.mkdir()
        monkeypatch.setenv("HOME", str(homedir))
        monkeypatch.setenv("USERPROFILE", str(homedir))
        yield homedir

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
        # noinspection PyUnresolvedReferences
        assert config.Default.a == "alpha"
        # noinspection PyUnresolvedReferences
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

    def test_load__from_homedir(self, temp_home_dir: Path):
        path = temp_home_dir / "a.toml"
        with path.open(mode="wt") as f:
            f.write("[default]\n")
            f.write("a = 'alpha'")

        config = LayeredConfig.load("~/a.toml")

        assert config == {"default": {"a": "alpha"}}
