# PDF Image Extractor MCP Server

A Model Context Protocol (MCP) server that extracts images from PDF files. Run this locally to let LLMs access and analyze images embedded within your local PDF documents.

## Quick Start

You can run this server directly using `uvx` (part of the [uv](https://github.com/astral-sh/uv) toolkit). No manual installation required.

```bash
uvx pdf-image-extractor-mcp
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
      "args": ["pdf-image-extractor-mcp"]
    }
  }
}
```

### Cursor

To add this to [Cursor](https://cursor.com):

1.  Open Cursor Settings.
2.  Go to **Features** -> **MCP**.
3.  Click **+ Add New MCP Server**.
4.  Enter the following:
    *   **Name**: `pdf-image-extractor`
    *   **Type**: `stdio` (or Command)
    *   **Command**: `uvx pdf-image-extractor-mcp`

### VS Code

If you are using the [MCP Extension for VS Code](https://marketplace.visualstudio.com/items?itemName=Anthropic.mcp-server) (or a compatible AI extension):

Create or edit `.vscode/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "pdf-image-extractor": {
      "command": "uvx",
      "args": ["pdf-image-extractor-mcp"]
    }
  }
}
```

### Claude Code (CLI)

To add this server to [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview):

```bash
claude mcp add pdf-image-extractor -- uvx pdf-image-extractor-mcp
```

### n8n

To use this with [n8n](https://n8n.io):

**Note**: n8n typically connects to MCP servers via HTTP (SSE), not local commands (`stdio`). To use this server with n8n, you must run it behind a generic SSE adapter.

1.  Install the **n8n-nodes-mcp** community node in your n8n instance.
2.  Run this server wrapped in an SSE transport (using a tool like `mcp-proxy` or `stdio-to-sse`).
3.  Configure the n8n MCP Client node to point to your local SSE port (e.g., `http://localhost:3000/sse`).

## Development

If you want to contribute or run from source, please see [CONTRIBUTING.md](CONTRIBUTING.md).