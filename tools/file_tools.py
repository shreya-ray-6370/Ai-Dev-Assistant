from pathlib import Path
from langchain_core.tools import tool

UPLOADS_DIR = Path("uploads")


@tool
def read_uploaded_file(filename: str) -> str:
    """
    Read the contents of an uploaded text/code file.

    Use this when:
    - user asks to explain code
    - debug code
    - optimize file
    - analyze implementation

    Input:
    - filename: exact uploaded filename

    Returns:
    - file contents as text
    """

    file_path = UPLOADS_DIR / filename

    if not file_path.exists():
        return f"File not found: {filename}"

    try:
        content = file_path.read_text(encoding="utf-8")
        return content

    except Exception:
        return f"Could not read file: {filename}"