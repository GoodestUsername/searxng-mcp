from fastmcp import FastMCP
from searxng_client import SearxngClient


def create_mcp_server(api_url: str) -> FastMCP:
    mcp = FastMCP("Searxng")
    searxng_client = SearxngClient(api_url)

    mcp.tool(searxng_client.search)

    return mcp
