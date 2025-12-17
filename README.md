# PDF Image Extractor MCP Server

A Model Context Protocol (MCP) server that extracts images from PDF files. This server runs locally on your machine, allowing LLMs to access and analyze images embedded within your local PDF documents.

## Features

-   **Local File Access**: smart searching for PDFs in your current directory, Downloads, Desktop, or temp folder.
-   **Pagination**: Efficiently handles PDFs with many images by extracting them in batches.
-   **Native Processing**: Uses `PyMuPDF` for high-fidelity extraction.

## Installation

This server is designed to be run with `uv`.

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/maxrabin/pdf-image-extractor-mcp.git
    cd pdf-image-extractor-mcp
    ```

2.  **Install dependencies**:
    ```bash
    uv sync
    ```

## Usage & Configuration

This server communicates via `stdio` (standard input/output), meaning it must be run as a local command by your MCP client.

### Claude Desktop Configuration

Edit your `claude_desktop_config.json` (usually located at `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "pdf-image-extractor": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/ABSOLUTE/PATH/TO/pdf-image-extractor-mcp",
        "pdf-image-extractor-mcp"
      ]
    }
  }
}
```
*Replace `/ABSOLUTE/PATH/TO/` with the actual path to where you cloned this repository.*

### Cursor Configuration

1.  Open Cursor Settings.
2.  Navigate to **Features** -> **MCP**.
3.  Click **+ Add New MCP Server**.
4.  Enter the following:
    *   **Name**: `pdf-image-extractor` (or any name you prefer)
    *   **Type**: `stdio` (or Command)
    *   **Command**: `uv run --directory /ABSOLUTE/PATH/TO/pdf-image-extractor-mcp pdf-image-extractor-mcp`

### Testing Locally

You can verify the server works by running it directly from the command line. It should wait for input without crashing:

```bash
uv run pdf-image-extractor-mcp
```
*(You won't see output until you send a valid JSON-RPC message, but it verifies the startup)*

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development instructions.
