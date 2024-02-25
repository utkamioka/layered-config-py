from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import MutableMapping, Mapping

import toml

from .attribute_accessor import AttributeAccessor

logger = logging.getLogger(__name__)


class LayeredConfig:
    @classmethod
    def load(cls, *args: str | os.PathLike | Mapping) -> AttributeAccessor:
        config = dict()

        for arg in args:
            if isinstance(arg, Mapping):
                obj = arg
            else:
                obj = cls._load_file_if_exists(path=arg)

            if obj:
                cls._merge_dicts(config, obj)

        return AttributeAccessor.get(config)

    @classmethod
    def _load_file_if_exists(cls, path: str | os.PathLike) -> MutableMapping | None:
        path = Path(path)
        if path.exists():
            logger.debug("Loading configuration from %s", path)
            return toml.load(path)

    @classmethod
    def _merge_dicts(cls, dict1: MutableMapping, dict2: Mapping) -> MutableMapping:
        for key in dict2:
            if key in dict1:
                if isinstance(dict1[key], MutableMapping) and isinstance(dict2[key], Mapping):
                    cls._merge_dicts(dict1[key], dict2[key])
                else:
                    dict1[key] = dict2[key]
            else:
                dict1[key] = dict2[key]
        return dict1
