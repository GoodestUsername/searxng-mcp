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
    api_url = os.environ.get("SEARXNG_URL", "http://host.docker.internal:8181")
    default_path = os.environ.get("DEFAULT_PATH", "mcp")

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
                path=f"/{path if path != None else default_path}",
                stateless_http=stateless_http,
            )
        )

    app()


if __name__ == "__main__":
    main()
