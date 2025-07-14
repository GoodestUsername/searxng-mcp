# MCP Server for SearXNG

This project provides an MCP (Multi-Client Protocol) server interface for interacting with [SearXNG](https://github.com/searxng/searxng), the privacy-respecting meta-search engine. The server allows programmatic access to search functionality through a standardized protocol.

## Features

- Integration with SearXNG
- Support for multiple transport protocols (stdio, HTTP)
- Type-safe API using Pydantic models
- Flexible configuration via environment variables
- Docker support for easy deployment

## Prerequisites

Before running the server:
1. Ensure you have a working [SearXNG](https://github.com/searxng/searxng) instance (local or remote)
2. Install Python 3.13+ and required dependencies:
   ```bash
   uv sync
   ```

### Environment Variables

| Variable     | Default Value          | Description                        |
|--------------|------------------------|------------------------------------|
| SEARXNG_URL  | `http://localhost:8181`| URL of the SearxNG instance        |
| DEFAULT_PATH | `mcp`              | Default path of in the uri if none is provided        |

### Command Line Interface

The application provides a Typer-based CLI with two main commands:

#### stdio mode
```bash
python searxng_mcp/main.py stdio
```

#### http mode
```bash
python searxng_mcp/main.py http --host=0.0.0.0 --port=8000
```

### Docker

Build the image:
```bash
docker build --tag 'mcp/searxng-mcp' .
```

Run in stdio mode:
```bash
docker run mcp/searxng-mcp stdio
```

Run in HTTP mode (exposing port 8000):
```bash
docker run -p 8000:8000 mcp/searxng-mcp http --host=0.0.0.0 --port=8000
```
## MCP Config file examples
#### With http:
```json
{
  "mcpServers": {
    "mcp/searxng": {
      "url": "http://0.0.0.0:8000/mcp"
    }
  }
}
```

#### With stdio:
```json
{
  "mcpServers": {
    "mcp/searxng": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "mcp/searxng-mcp",
        "stdio"
      ]
    }
  }
}
```

## API Documentation

The server implements a MCP (Model Communication Protocol) compatible with FastMCP.

### Search Tool
- **Name**: `search`
- **Description**: Performs a search query using a remote SearXNG instance.
- **Parameters**:
  - `q` (str): The search query string. Supports advanced syntax per engine.
  - `categories` (list[Categories], optional): List of active categories. See available in code.
  - `engines` (list[Engines], optional): List of specific engines to use.
  - `language` (str, optional): ISO language code for results.
  - `pageno` (int, default=1): Page number starting from 1.
  - `time_range` (Literal['day','month','year'], optional): Time range filter.
  - `format` (Literal['html', 'json', 'csv', 'rss'], default='json'): Output format.
  - `image_proxy` (bool, optional): Proxy images through SearXNG?
  - `safesearch` (int:0-2, optional): Safe search level. Higher is stricter.
  - `enabled_plugins`, `disabled_plugins` (list[Plugins], optional): Plugins to enable/disable.
  - `enabled_engines`, `disabled_engines` (list[Engines], optional): Engines to enable/disable.

- **Returns**:
  - Structured JSON, CSV as a list of rows or raw text depending on the format requested.
  - CSV and raw are returned as json with a single key named "output"

