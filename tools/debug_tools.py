from langchain_core.tools import tool
from tools.file_tools import read_uploaded_file


@tool
def detect_missing_imports(filename: str) -> str:
    print(f"Detecting missing imports for file: {filename}")
    """
    Analyze a file for possible missing imports.
    """

    content = read_uploaded_file.invoke({
        "filename": filename
    })

    return f"""
Analyze this code for missing imports:

{content}
"""


@tool
def detect_bug_patterns(filename: str) -> str:
    print(f"Detecting bug patterns for file: {filename}")
    """
    Analyze uploaded code for common bug patterns.
    """

    content = read_uploaded_file.invoke({
        "filename": filename
    })

    return f"""
Analyze this code for:
- syntax issues
- logical bugs
- runtime issues
- bad practices

Code:

{content}
"""


debug_tools = [
    read_uploaded_file,
    detect_missing_imports,
    detect_bug_patterns
]