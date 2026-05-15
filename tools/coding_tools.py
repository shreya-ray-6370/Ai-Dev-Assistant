from langchain_core.tools import tool
from tools.file_tools import read_uploaded_file


@tool
def explain_code_structure(filename: str) -> str:
    print(f"Explaining code structure for file: {filename}")
    """
    Read a code file and explain its structure,
    functions, classes, and major logic blocks.
    """

    return read_uploaded_file.invoke({
        "filename": filename
    })


@tool
def generate_component_template(component_name: str) -> str:
    print(f"Generating component template for: {component_name}")
    """
    Generate a frontend component template.
    Useful for React component scaffolding.
    """

    return f"""
function {component_name}() {{
    return (
        <div>
            {component_name}
        </div>
    )
}}

export default {component_name}
"""


coding_tools = [
    read_uploaded_file,
    explain_code_structure,
    generate_component_template
]