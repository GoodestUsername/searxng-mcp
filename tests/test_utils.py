import pytest
from fastmcp.exceptions import ToolError

from searxng_mcp.searxng_client import Engines, parse_args


def test_parse_args_required_field_missing():
    def dummy_func(x: int, y: str):
        pass

    with pytest.raises(ToolError) as e:
        parse_args(dummy_func, {"x": 1})  # missing 'y'
    assert "y" in str(e.value)


def test_parse_args_with_enum_list():
    def dummy_func(engine_list: list[Engines]):
        pass

    raw = {"engine_list": [Engines.google, Engines.duckduckgo]}
    result = parse_args(dummy_func, raw)

    assert result["engine_list"] == "google, duckduckgo"


def test_parse_args_optional_empty_skipped():
    def dummy_func(a: int, b: str = "default"):
        pass

    raw = {"a": 42, "b": ""}
    result = parse_args(dummy_func, raw)

    assert result == {"a": 42}
