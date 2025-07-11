import os
from enum import Enum
from functools import partial

import anyio
import typer
from server import create_mcp_server


class HTTPTransportTypes(Enum):
    http = "http"
    streamable_http = "streamable-http"
    sse = "sse"


def main():
    api_url = os.environ.get("SEARXNG_URL", "http://localhost:8181")
    mcp = create_mcp_server(api_url)

    app = typer.Typer()

    @app.command()
    def stdio(show_banner: bool = True):
        anyio.run(
            partial(
                mcp.run_stdio_async,
                show_banner=show_banner,
            )
        )

    @app.command()
    def http(
        show_banner: bool = True,
        transport: HTTPTransportTypes = HTTPTransportTypes.http,
        host: str | None = None,
        port: int | None = None,
        log_level: str | None = None,
        path: str | None = None,
        stateless_http: bool | None = None,
    ):
        anyio.run(
            partial(
                mcp.run_http_async,
                show_banner=show_banner,
                transport=transport.value,
                host=host,
                port=port,
                log_level=log_level,
                path=path,
                stateless_http=stateless_http,
            )
        )

    app()


if __name__ == "__main__":
    main()
