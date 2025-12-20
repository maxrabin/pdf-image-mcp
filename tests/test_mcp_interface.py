import os
from pathlib import Path
from typing import Any, cast

import fitz  # type: ignore[import-untyped]
import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import ImageContent, TextContent


def create_dummy_pdf(path: str) -> None:
    """Creates a PDF with a simple red rectangle image."""
    doc = fitz.open()
    page = doc.new_page()
    pix = fitz.Pixmap(fitz.csRGB, (0, 0, 10, 10), False)
    img_data = pix.tobytes("png")  # type: ignore
    rect = fitz.Rect(100, 100, 200, 200)
    page.insert_image(rect, stream=img_data)  # type: ignore
    doc.save(path)  # type: ignore
    doc.close()


@pytest.mark.asyncio
async def test_mcp_list_tools():
    """Test that the MCP server lists tools with correct descriptions."""
    # Run the server from the local source
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "pdf_image_extractor_mcp.main"],
        env={**os.environ, "PYTHONPATH": "src"},
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools_result = await session.list_tools()
            tools = tools_result.tools

            assert len(tools) > 0
            tool = next((t for t in tools if t.name == "extract_pdf_images"), None)
            assert tool is not None
            assert tool.description is not None
            assert "Extract images from a PDF file" in tool.description

            # Verify parameter descriptions are present (the fix we made)
            properties = cast(dict[str, Any], tool.inputSchema.get("properties", {}))
            assert "pdf_full_path" in properties
            assert "description" in properties["pdf_full_path"]
            assert "absolute path" in properties["pdf_full_path"]["description"]


@pytest.mark.asyncio
async def test_mcp_call_tool(tmp_path: Path):
    """Test calling the tool via the MCP protocol."""
    pdf_path = tmp_path / "test_mcp.pdf"
    create_dummy_pdf(str(pdf_path))

    server_params = StdioServerParameters(
        command="python",
        args=["-m", "pdf_image_extractor_mcp.main"],
        env={**os.environ, "PYTHONPATH": "src"},
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Call the tool
            result = await session.call_tool(
                "extract_pdf_images", arguments={"pdf_full_path": str(pdf_path)}
            )

            # Check structure of the result
            assert not result.isError
            content = result.content
            assert len(content) >= 2

            # First part should be summary text
            assert isinstance(content[0], TextContent)
            assert "Extracted 1 images" in content[0].text

            # Second part should be an image
            assert isinstance(content[1], ImageContent)
            assert content[1].mimeType == "image/png"
            assert len(content[1].data) > 0
