import os

from fastmcp import FastMCP

URL = os.environ.get("SEARXNG_URL", "http://localhost:8000")
mcp = FastMCP("Searxng")


@mcp.tool
def hi():
    return "hello world"


def main():
    mcp.run()


if __name__ == "__main__":
    main()
