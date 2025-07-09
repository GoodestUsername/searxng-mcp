from fastmcp import FastMCP
import os

URL = os.environ.get("SEARXNG_URL", "http://localhost:8000")
mcp = FastMCP("Searxing")


def main():
    mcp.run()


if __name__ == "__main__":
    main()
