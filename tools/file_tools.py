from pathlib import Path
from langchain_core.tools import tool
from PIL import Image

UPLOADS_DIR = Path("uploads")


@tool
def list_uploaded_files() -> str:
    """List all uploaded files."""
    if not UPLOADS_DIR.exists():
        return "No uploads folder found."

    files = []
    for file in UPLOADS_DIR.iterdir():
        if file.is_file():
            files.append(file.name)

    if not files:
        return "No uploaded files found."

    return "\n".join(files)


@tool
def read_uploaded_file(filename: str) -> str:
    """Read an uploaded text/code file."""
    file_path = UPLOADS_DIR / filename

    if not file_path.exists():
        return f"File not found: {filename}"

    try:
        content = file_path.read_text(encoding="utf-8")
        return content
    except Exception:
        return f"Could not read file: {filename}"


@tool
def inspect_image(filename: str) -> str:
    """Inspect an uploaded image and return basic details."""
    file_path = UPLOADS_DIR / filename

    if not file_path.exists():
        return f"Image not found: {filename}"

    try:
        image = Image.open(file_path)
        return (
            f"Image name: {filename}, "
            f"format: {image.format}, "
            f"size: {image.size}, "
            f"mode: {image.mode}"
        )
    except Exception:
        return f"Could not inspect image: {filename}"


tools = [list_uploaded_files, read_uploaded_file, inspect_image]