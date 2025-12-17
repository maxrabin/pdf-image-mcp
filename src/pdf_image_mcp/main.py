"""MCP server for extracting images from PDFs using PyMuPDF."""

import base64
import os
import tempfile
from dataclasses import dataclass
from typing import Annotated, Any, cast

import fitz  # type: ignore[import-untyped]
from mcp.server.fastmcp import FastMCP, Image

# Initialize FastMCP server
mcp = FastMCP("pdf-image-extractor-mcp")


@dataclass
class ImageInfo:
    """Information about an extracted image."""

    page: int
    index: int
    filename: str
    filepath: str
    base64: str
    media_type: str


def find_pdf_path(
    pdf_path: str,
) -> str | None:
    """
    Find the actual path of the PDF file by checking multiple locations.

    Args:
        pdf_path: The provided path or filename.

    Returns:
        The absolute path if found, otherwise None.
    """
    possible_paths = [
        pdf_path,  # Direct path as provided
        os.path.join(os.getcwd(), pdf_path),  # Current working directory
        os.path.join(os.path.expanduser("~"), "Downloads", pdf_path),  # Downloads
        os.path.join(os.path.expanduser("~"), "Desktop", pdf_path),  # Desktop
        os.path.join(tempfile.gettempdir(), pdf_path),  # Temp directory
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None


def extract_images_logic(
    pdf_path: str,
    start_index: int = 0,
    max_images: int = 10,
) -> list[Any]:
    """
    Core logic to extract images from a PDF file.
    """
    actual_path = find_pdf_path(pdf_path)

    if not actual_path:
        return [f"Error: PDF file not found: {pdf_path}"]

    output_dir = tempfile.gettempdir()
    all_images: list[ImageInfo] = []

    try:
        # Open the document
        doc = fitz.open(actual_path)
    except Exception as e:
        return [f"Error opening PDF file: {str(e)}"]

    try:
        # First pass: collect all images with their page info
        for page_num in range(len(doc)):
            page = doc[page_num]
            # get_images() returns a list of tuples, but pyright doesn't know that
            page_images = cast(list[Any], page.get_images())

            for img_index, img in enumerate(page_images):
                xref = cast(int, img[0])
                try:
                    pix = fitz.Pixmap(doc, xref)

                    # Convert CMYK to RGB if necessary
                    if pix.n - pix.alpha < 4:  # type: ignore
                        pass
                    else:
                        pix = fitz.Pixmap(fitz.csRGB, pix)

                    # Save image
                    filename = f"page_{page_num:03d}_img_{img_index:02d}.png"
                    filepath = os.path.join(output_dir, filename)
                    pix.save(filepath)  # type: ignore[no-any-return]

                    # Read and encode as base64
                    with open(filepath, "rb") as f:
                        img_data = f.read()
                        b64_data = base64.b64encode(img_data).decode("utf-8")

                    all_images.append(
                        ImageInfo(
                            page=page_num,
                            index=img_index,
                            filename=filename,
                            filepath=filepath,
                            base64=b64_data,
                            media_type="image/png",
                        )
                    )
                except Exception as e:
                    # Log error for this specific image but continue
                    print(f"Error extracting image {img_index} on page {page_num}: {e}")
                    continue

    except Exception as e:
        return [f"Error processing PDF structure: {str(e)}"]
    finally:
        if "doc" in locals():
            doc.close()

    # Apply pagination
    total_available = len(all_images)
    end_index = min(start_index + max_images, total_available)
    paginated_images = all_images[start_index:end_index]
    has_more = end_index < total_available

    # Construct response
    content: list[Any] = []

    # Add summary text
    summary = (
        f"Extracted {len(paginated_images)} images "
        f"(showing {start_index}-{end_index - 1} of {total_available} total)."
    )
    if has_more:
        summary += (
            f"\n\n⚠️ **IMPORTANT: There are more images.** "
            f"Request next batch: start_index={end_index} max_images={max_images}"
        )
    else:
        summary += "\n\n✓ **All images extracted.**"

    content.append(summary)

    # Add images
    for img_info in paginated_images:
        content.append(Image(data=base64.b64decode(img_info.base64), format="png"))

    return content


@mcp.tool()
def extract_pdf_images(
    pdf_path: Annotated[
        str,
        "The exact filename of the uploaded PDF (e.g., 'report.pdf'). "
        "Do NOT include directory paths.",
    ],
    start_index: Annotated[
        int, "Starting index for pagination (0-based). Default is 0."
    ] = 0,
    max_images: Annotated[
        int,
        "Maximum number of images to extract. Recommended: 10. Default: 10.",
    ] = 10,
) -> list[Any]:
    """
    Extract images from a PDF file with pagination.

    Works best when extracting small batches of images (e.g., 10) at a time.
    Returns a list of image contents and a summary message.
    """
    return extract_images_logic(pdf_path, start_index, max_images)


def main() -> None:
    """Entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
