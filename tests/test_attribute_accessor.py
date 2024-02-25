from collections import OrderedDict

import pytest

from layered_config.attribute_accessor import AttributeAccessor


class TestAttributeAccessor:
    def test_get__with_dict(self):
        obj = AttributeAccessor.get({"a": {"b": {"c": {"d": "delta"}}}})

        assert obj == {"a": {"b": {"c": {"d": "delta"}}}}
        assert obj.a == {"b": {"c": {"d": "delta"}}}
        assert obj.a.b == {"c": {"d": "delta"}}
        assert obj.a.b.c == {"d": "delta"}
        assert obj.a.b.c.d == "delta"

        with pytest.raises(AttributeError) as excinfo:
            _ = obj.xxx
        assert excinfo.value.args[0] == "'AttributeMapping' object has no attribute 'xxx'"

    def test_get__with_ordered_dict(self):
        obj = AttributeAccessor.get(OrderedDict(a=OrderedDict(b=OrderedDict(c="charlie"))))

        assert obj == {"a": {"b": {"c": "charlie"}}}
        assert obj.a == {"b": {"c": "charlie"}}
        assert obj.a.b == {"c": "charlie"}
        assert obj.a.b.c == "charlie"

    def test_get__with_list(self):
        obj = AttributeAccessor.get([0, {"a": {"b": "bravo"}}, 2])

        assert obj == [0, {"a": {"b": "bravo"}}, 2]
        assert obj[0] == 0
        assert obj[1] == {"a": {"b": "bravo"}}
        assert obj[1].a == {"b": "bravo"}
        assert obj[1].a.b == "bravo"
        assert obj[2] == 2

    def test_get__with_tuple(self):
        obj = AttributeAccessor.get((0, {"a": {"b": "bravo"}}, 2))

        assert obj == [0, {"a": {"b": "bravo"}}, 2]
        assert obj[1].a.b == "bravo"

    def test_get__with_scalar_value(self):
        assert AttributeAccessor.get(0) == 0
        assert AttributeAccessor.get(0.1) == 0.1
        assert AttributeAccessor.get("abc") == "abc"
        assert AttributeAccessor.get(True) is True
        assert AttributeAccessor.get(False) is False
        assert AttributeAccessor.get(None) is None
