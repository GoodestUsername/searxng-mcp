import json

import pytest
from fastmcp.tools.tool import ToolResult
from httpx import URL, HTTPStatusError, RequestError
from mcp.types import TextContent
from pytest_httpx import HTTPXMock

from searxng_mcp.searxng_client import Categories, Engines, Plugins, SearxngClient

MOCK_SEARXNG_URL = "https://mocksearxng.com"


@pytest.mark.asyncio
async def test_full_json_query(httpx_mock: HTTPXMock):
    client = SearxngClient(api_url=MOCK_SEARXNG_URL)

    expected_result = {
        "results": [{"title": "Hello World", "url": "https://example.com"}]
    }
    params = {
        "q": "Hello World",
        "categories": "general",
        "engines": "google",
        "pageno": 1,
        "format": "json",
        "time_range": "day",
        "language": "en",
        "safesearch": 1,
        "enabled_plugins": "Hash_plugin",
        "disabled_plugins": Plugins.vim_like_hotkeys.value,
        "enabled_engines": "google",
        "disabled_engines": "bing",
        "image_proxy": True,
    }

    httpx_mock.add_response(
        method="GET",
        url=URL(MOCK_SEARXNG_URL + "/search", params=params),
        text=json.dumps(expected_result),
        headers={"Content-Type": "application/json"},
    )

    result = await client.search(
        q="Hello World",
        categories=[Categories.general],
        engines=[Engines.google],
        pageno=1,
        format="json",
        time_range="day",
        language="en",
        safesearch=1,
        enabled_plugins=[Plugins.hash_plugin],
        disabled_plugins=[Plugins.vim_like_hotkeys],
        enabled_engines=[Engines.google],
        disabled_engines=[Engines.bing],
        image_proxy=True,
    )

    assert isinstance(result, ToolResult)
    if result.structured_content is None:
        pytest.fail("Structure content is None.")

    assert "results" in result.structured_content
    assert result.structured_content["results"][0]["title"] == "Hello World"


@pytest.mark.asyncio
async def test_html_fallback_format(httpx_mock: HTTPXMock):
    client = SearxngClient(api_url=MOCK_SEARXNG_URL)

    params = {"q": "fallback test", "format": "html", "pageno": 1}
    html_content = "<html><body><h1>Test</h1></body></html>"

    httpx_mock.add_response(
        method="GET",
        url=URL(MOCK_SEARXNG_URL + "/search", params=params),
        text=html_content,
        headers={"Content-Type": "text/html"},
    )

    result = await client.search(q="fallback test", format="html")
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)
    assert "Test" in result.content[0].text


@pytest.mark.asyncio
async def test_csv_format(httpx_mock: HTTPXMock):
    client = SearxngClient(api_url=MOCK_SEARXNG_URL)
    params = {"q": "some csv query", "format": "csv", "pageno": 1}

    csv_data = "title,url\nExample Title,https://example.com\n"
    httpx_mock.add_response(
        method="GET",
        url=URL(MOCK_SEARXNG_URL + "/search", params=params),
        text=csv_data,
        headers={"Content-Type": "text/html"},
    )

    result = await client.search(q="some csv query", format="csv")

    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)
    rows = json.loads(result.content[0].text)["output"]
    assert rows[0] == ["title", "url"]
    assert rows[1] == ["Example Title", "https://example.com"]


@pytest.mark.asyncio
async def test_minimal_parameters_only(httpx_mock: HTTPXMock):
    client = SearxngClient(api_url=MOCK_SEARXNG_URL)
    params = {"q": "minimal test", "format": "json", "pageno": 1}
    data = {"results": [{"title": "Minimal", "url": "https://min.example"}]}

    httpx_mock.add_response(
        method="GET",
        url=URL(MOCK_SEARXNG_URL + "/search", params=params),
        text=json.dumps(data),
        headers={"Content-Type": "text/html"},
    )

    result = await client.search(q="minimal test", format="json")
    assert isinstance(result, ToolResult)
    if result.structured_content is None:
        pytest.fail("Structure content is None.")

    assert "results" in result.structured_content
    assert result.structured_content["results"][0]["title"] == "Minimal"


@pytest.mark.asyncio
async def test_invalid_format_gracefully_fallback(httpx_mock: HTTPXMock):
    client = SearxngClient(api_url=MOCK_SEARXNG_URL)

    fallback_text = "some text fallback from API"
    params = {"q": "weird format", "format": "weird", "pageno": 1}

    httpx_mock.add_response(
        method="GET",
        url=URL(MOCK_SEARXNG_URL + "/search", params=params),
        text=fallback_text,
        headers={"Content-Type": "text/html"},
    )

    result = await client.search(
        q="weird format",
        format="weird",  # type: ignore
    )
    assert isinstance(result, ToolResult)
    assert isinstance(result.content[0], TextContent)
    assert fallback_text in result.content[0].text


@pytest.mark.asyncio
async def test_invalid_url_raises(httpx_mock: HTTPXMock):
    client = SearxngClient(api_url=MOCK_SEARXNG_URL)
    params = {"q": "not found", "format": "json", "pageno": 1}

    httpx_mock.add_response(
        method="GET",
        url=URL(MOCK_SEARXNG_URL + "/search", params=params),
        status_code=404,
        text="Not Found",
        headers={"Content-Type": "text/html"},
    )
    with pytest.raises(HTTPStatusError):
        await client.search(q="not found", format="json")


@pytest.mark.asyncio
async def test_network_error(httpx_mock: HTTPXMock):
    client = SearxngClient(api_url=MOCK_SEARXNG_URL)

    def raise_request_error(request):
        raise RequestError("Connection failed", request=request)

    httpx_mock.add_callback(raise_request_error)

    with pytest.raises(RequestError):
        await client.search(q="timeout test", format="json")
