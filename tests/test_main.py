from pathlib import Path
from typing import cast

import fitz  # type: ignore
import pytest
from mcp.types import ImageContent, TextContent

from pdf_image_extractor_mcp.main import extract_images_logic


def create_dummy_pdf_bytes() -> bytes:
    """Creates a PDF with a simple red rectangle image and returns bytes."""
    doc = fitz.open()
    page = doc.new_page()
    pix = fitz.Pixmap(fitz.csRGB, (0, 0, 10, 10), False)
    img_data = pix.tobytes("png")  # type: ignore
    rect = fitz.Rect(100, 100, 200, 200)
    page.insert_image(rect, stream=img_data)  # type: ignore
    pdf_bytes = cast(bytes, doc.tobytes())  # type: ignore
    doc.close()
    return pdf_bytes


def create_dummy_pdf(path: str) -> None:
    """Creates a PDF with a simple red rectangle image."""
    pdf_bytes = create_dummy_pdf_bytes()
    with open(path, "wb") as f:
        f.write(pdf_bytes)


@pytest.mark.asyncio
async def test_extract_images_success(tmp_path: Path) -> None:
    # Create a dummy PDF in the temp directory
    pdf_path = tmp_path / "test.pdf"
    create_dummy_pdf(str(pdf_path))

    # Run extraction
    results = await extract_images_logic(pdf_full_path=str(pdf_path))

    # Check results
    assert len(results) >= 2  # Summary + 1 image
    assert isinstance(results[0], TextContent)
    assert "Extracted 1 images" in results[0].text

    # Check if the second item is an ImageContent object
    img = results[1]
    assert isinstance(img, ImageContent)
    assert img.mimeType == "image/png"
    assert len(img.data) > 0


@pytest.mark.asyncio
async def test_extract_images_file_not_found() -> None:
    results = await extract_images_logic(pdf_full_path="nonexistent.pdf")
    assert len(results) == 1
    assert "Error: PDF file not found" in results[0].text


@pytest.mark.asyncio
async def test_extract_images_pagination(tmp_path: Path) -> None:
    # Create a PDF with 2 images
    pdf_path = tmp_path / "test_multi.pdf"
    doc = fitz.open()
    page = doc.new_page()
    pix = fitz.Pixmap(fitz.csRGB, (0, 0, 10, 10), False)
    img_data = pix.tobytes("png")  # type: ignore
    page.insert_image(fitz.Rect(0, 0, 50, 50), stream=img_data)  # type: ignore
    page.insert_image(fitz.Rect(50, 50, 100, 100), stream=img_data)  # type: ignore
    doc.save(str(pdf_path))  # type: ignore
    doc.close()

    # Extract with max_images=1
    results = await extract_images_logic(pdf_full_path=str(pdf_path), max_images=1)

    assert len(results) == 2
    assert isinstance(results[0], TextContent)
    assert "Extracted 1 images" in results[0].text
    assert "IMPORTANT: There are more images" in results[0].text

    # Extract next batch
    results2 = await extract_images_logic(
        pdf_full_path=str(pdf_path), start_index=1, max_images=1
    )
    assert len(results2) == 2
    assert isinstance(results2[0], TextContent)
    assert "Extracted 1 images" in results2[0].text
    assert "All images extracted" in results2[0].text
