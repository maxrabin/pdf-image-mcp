from pathlib import Path
from typing import Any, cast

import fitz  # type: ignore
from mcp.server.fastmcp import Image

from pdf_image_extractor_mcp.main import extract_images_logic


def create_dummy_pdf(path: str) -> None:
    """Creates a PDF with a simple red rectangle image."""
    doc = fitz.open()
    page = doc.new_page()

    # Create a simple image programmatically (defaults to black)
    pix = fitz.Pixmap(fitz.csRGB, (0, 0, 10, 10), False)
    img_data = pix.tobytes("png")  # type: ignore

    rect = fitz.Rect(100, 100, 200, 200)
    page.insert_image(rect, stream=img_data)  # type: ignore

    doc.save(path)  # type: ignore
    doc.close()


def test_extract_images_success(tmp_path: Path) -> None:
    # Create a dummy PDF in the temp directory
    pdf_path = tmp_path / "test.pdf"
    create_dummy_pdf(str(pdf_path))

    # Run extraction
    results = extract_images_logic(str(pdf_path))

    # Check results
    assert len(results) >= 2  # Summary + 1 image
    assert isinstance(results[0], str)
    assert "Extracted 1 images" in results[0]

    # Check if the second item is an Image object
    img = results[1]
    assert isinstance(img, Image)

    # Cast to Any to check attributes that might not be statically defined
    img_any = cast(Any, img)

    # Check attributes (FastMCP Image vs ImageContent)
    if hasattr(img_any, "format"):
        assert img_any.format == "png"
    elif hasattr(img_any, "mimeType"):
        assert img_any.mimeType == "image/png"

    # Handle Optional[bytes] for data
    assert img.data is not None
    assert len(img.data) > 0


def test_extract_images_file_not_found() -> None:
    results = extract_images_logic("nonexistent.pdf")
    assert len(results) == 1
    assert "Error: PDF file not found" in results[0]


def test_extract_images_pagination(tmp_path: Path) -> None:
    # Create a PDF with 2 images (on same or different pages)
    pdf_path = tmp_path / "test_multi.pdf"
    doc = fitz.open()
    page = doc.new_page()

    # Create valid image data
    pix = fitz.Pixmap(fitz.csRGB, (0, 0, 10, 10), False)
    img_data = pix.tobytes("png")  # type: ignore

    # Insert twice
    page.insert_image(fitz.Rect(0, 0, 50, 50), stream=img_data)  # type: ignore
    page.insert_image(fitz.Rect(50, 50, 100, 100), stream=img_data)  # type: ignore

    doc.save(str(pdf_path))  # type: ignore
    doc.close()

    # Extract with max_images=1
    results = extract_images_logic(str(pdf_path), max_images=1)

    # Should get summary + 1 image
    assert len(results) == 2
    assert "Extracted 1 images" in results[0]
    assert "IMPORTANT: There are more images" in results[0]

    # Extract next batch
    results2 = extract_images_logic(str(pdf_path), start_index=1, max_images=1)
    assert len(results2) == 2
    assert "Extracted 1 images" in results2[0]
    assert "All images extracted" in results2[0]
