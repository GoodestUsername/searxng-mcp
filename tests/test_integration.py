# based off: https://github.com/jlowin/fastmcp/blob/main/tests/integration_tests/test_github_mcp_remote.py

import os

import pytest
from fastmcp import Client
from fastmcp.client import StreamableHttpTransport
from fastmcp.exceptions import ToolError
from fastmcp.tools.tool import ToolResult
from mcp.types import Tool

# TODO: put this in env out of Dockerfile
SEARXNG_MCP_URL = "http://127.0.0.1:8000/mcp/"
PATH = os.environ.get("DEFAULT_PATH", "mcp")


@pytest.fixture(name="streamable_http_client")
def fixture_streamable_http_client() -> Client[StreamableHttpTransport]:
    return Client(
        StreamableHttpTransport(
            url=SEARXNG_MCP_URL,
        )
    )


@pytest.mark.asyncio
async def test_connect_disconnect(
    streamable_http_client: Client[StreamableHttpTransport],
):
    async with streamable_http_client:
        assert streamable_http_client.is_connected() is True
        await streamable_http_client._disconnect()
        assert streamable_http_client.is_connected() is False


@pytest.mark.asyncio
async def test_ping(streamable_http_client: Client[StreamableHttpTransport]):
    """Test pinging the server."""
    async with streamable_http_client:
        assert streamable_http_client.is_connected() is True
        result = await streamable_http_client.ping()
        assert result is True


@pytest.mark.asyncio
async def test_list_tools(streamable_http_client: Client[StreamableHttpTransport]):
    """Test listing the MCP tools"""
    async with streamable_http_client:
        assert streamable_http_client.is_connected()
        tools = await streamable_http_client.list_tools()
        assert isinstance(tools, list)
        assert len(tools) > 0  # Ensure the tools list is non-empty
        for tool in tools:
            assert isinstance(tool, Tool)
            assert len(tool.name) > 0
            assert tool.description is not None and len(tool.description) > 0
            assert isinstance(tool.inputSchema, dict)
            assert len(tool.inputSchema) > 0


@pytest.mark.asyncio
async def test_list_resources(streamable_http_client: Client[StreamableHttpTransport]):
    """Test listing the MCP resources"""
    async with streamable_http_client:
        assert streamable_http_client.is_connected()
        resources = await streamable_http_client.list_resources()
        assert isinstance(resources, list)
        assert len(resources) == 0


@pytest.mark.asyncio
async def test_list_prompts(streamable_http_client: Client[StreamableHttpTransport]):
    """Test listing the MCP prompts"""
    async with streamable_http_client:
        assert streamable_http_client.is_connected()
        prompts = await streamable_http_client.list_prompts()
        assert len(prompts) == 0


@pytest.mark.asyncio
async def test_call_tool_ko(streamable_http_client: Client[StreamableHttpTransport]):
    """Test calling a non-existing tool"""
    async with streamable_http_client:
        assert streamable_http_client.is_connected()

        # Too unstable,the default message is already changed from the version in source.
        # with pytest.raises(ToolError, match="Unknown tool: foo"):
        with pytest.raises(ToolError):
            await streamable_http_client.call_tool("foo")


@pytest.mark.asyncio
async def test_call_tool_search(
    streamable_http_client: Client[StreamableHttpTransport],
):
    """Test calling search tool with minimal parameters"""
    async with streamable_http_client:
        assert streamable_http_client.is_connected()
        result = await streamable_http_client.call_tool("search", {"q": "naruto"})

    if result.structured_content is None:
        pytest.fail("Structure content is None.")

    assert isinstance(result.structured_content, dict)
    assert "results" in result.structured_content
    assert type(result.structured_content["results"]).__name__ == "list"
    assert len(result.structured_content["results"]) > 0


@pytest.mark.asyncio
async def test_call_tool_search_json(
    streamable_http_client: Client[StreamableHttpTransport],
):
    """Test calling search tool with json format"""
    async with streamable_http_client:
        assert streamable_http_client.is_connected()
        result = await streamable_http_client.call_tool(
            "search", {"q": "naruto", "format": "json"}
        )

    if result.structured_content is None:
        pytest.fail("Structure content is None.")

    assert isinstance(result.structured_content, dict)
    assert "results" in result.structured_content
    assert type(result.structured_content["results"]).__name__ == "list"
    assert len(result.structured_content["results"]) > 0


@pytest.mark.asyncio
async def test_call_tool_search_csv(
    streamable_http_client: Client[StreamableHttpTransport],
):
    """Test calling search tool with csv format"""
    async with streamable_http_client:
        assert streamable_http_client.is_connected()
        result = await streamable_http_client.call_tool(
            "search", {"q": "naruto", "format": "csv"}
        )

    if result.structured_content is None:
        pytest.fail("Structure content is None.")

    assert isinstance(result.structured_content, dict)
    assert "results" in result.structured_content
    assert type(result.structured_content["results"]).__name__ == "str"
    assert len(result.structured_content["results"]) > 0


@pytest.mark.asyncio
async def test_call_tool_search_html(
    streamable_http_client: Client[StreamableHttpTransport],
):
    """Test calling search tool with html format"""
    async with streamable_http_client:
        assert streamable_http_client.is_connected()
        result = await streamable_http_client.call_tool(
            "search", {"q": "naruto", "format": "html"}
        )

    if result.structured_content is None:
        pytest.fail("Structure content is None.")

    assert isinstance(result.structured_content, dict)
    assert "results" in result.structured_content
    assert type(result.structured_content["results"]).__name__ == "str"
    assert len(result.structured_content["results"]) > 0


@pytest.mark.asyncio
async def test_call_tool_search_rss(
    streamable_http_client: Client[StreamableHttpTransport],
):
    """Test calling search tool with rss format"""
    async with streamable_http_client:
        assert streamable_http_client.is_connected()
        result = await streamable_http_client.call_tool(
            "search", {"q": "naruto", "format": "rss"}
        )

    if result.structured_content is None:
        pytest.fail("Structure content is None.")

    assert isinstance(result.structured_content, dict)
    assert "results" in result.structured_content
    assert type(result.structured_content["results"]).__name__ == "str"
    assert len(result.structured_content["results"]) > 0
