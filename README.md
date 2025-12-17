# PDF Image Extractor MCP Server

[![PyPI](https://img.shields.io/pypi/v/pdf-image-extractor-mcp)](https://pypi.org/project/pdf-image-extractor-mcp/)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue?logo=python&logoColor=white)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/maxrabin/pdf-image-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/maxrabin/pdf-image-mcp/actions/workflows/ci.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A Model Context Protocol (MCP) server that extracts images from PDF files. Run this locally to let LLMs access and analyze images embedded within your local PDF documents.

## Quick Start

You can run this server directly using `uvx` (part of the [uv](https://github.com/astral-sh/uv) toolkit). No manual installation required.

```bash
uvx pdf-image-extractor-mcp@latest
```

## Configuration

### Claude Desktop app

To use this with the [Claude Desktop app](https://claude.ai/download), add the following to your `claude_desktop_config.json`:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "pdf-image-extractor": {
      "command": "uvx",
      "args": ["pdf-image-extractor-mcp@latest"]
    }
  }
}
```

### Cursor

To add this to [Cursor](https://cursor.com):

[![Install MCP Server](https://cursor.com/deeplink/mcp-install-light.svg)](https://cursor.com/en/install-mcp?name=pdf-image-extractor-mcp&config=eyJ0eXBlIjogInN0ZGlvIiwgImNvbW1hbmQiOiAidXZ4IiwgImFyZ3MiOiBbInBkZi1pbWFnZS1leHRyYWN0b3ItbWNwQGxhdGVzdCJdfQ==)

1.  Open Cursor Settings.
2.  Go to **Features** -> **MCP**.
3.  Click **+ Add New MCP Server**.
4.  Enter the following:
    *   **Name**: `pdf-image-extractor`
    *   **Type**: `stdio` (or Command)
    *   **Command**: `uvx pdf-image-extractor-mcp@latest`

### VS Code

If you are using the [MCP Extension for VS Code](https://marketplace.visualstudio.com/items?itemName=Anthropic.mcp-server) (or a compatible AI extension):

[![Install on VS Code](https://img.shields.io/badge/Install_on-VS_Code-FF9900?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=pdf-image-extractor-mcp&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22pdf-image-extractor-mcp%40latest%22%5D%7D)

Create or edit `.vscode/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "pdf-image-extractor": {
      "command": "uvx",
      "args": ["pdf-image-extractor-mcp@latest"]
    }
  }
}
```

### Claude Code (CLI)

To add this server to [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview):

```bash
claude mcp add pdf-image-extractor -- uvx pdf-image-extractor-mcp@latest
```

### n8n

To use this with [n8n](https://n8n.io):

**Note**: n8n typically connects to MCP servers via HTTP (SSE), not local commands (`stdio`). To use this server with n8n, you must run it behind a generic SSE adapter.

1.  Install the **n8n-nodes-mcp** community node in your n8n instance.
2.  Run this server wrapped in an SSE transport (using a tool like `mcp-proxy` or `stdio-to-sse`).
3.  Configure the n8n MCP Client node to point to your local SSE port (e.g., `http://localhost:3000/sse`).

## Development

If you want to contribute or run from source, please see [CONTRIBUTING.md](CONTRIBUTING.md).