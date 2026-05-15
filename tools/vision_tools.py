from langchain_core.tools import tool


@tool
def generate_ui_plan(ui_description: str) -> str:
    """
    Create a frontend implementation plan
    from UI screenshots or designs.
    """

    return f"""
Frontend UI Implementation Plan:

{ui_description}

Requirements:
- responsive layout
- reusable components
- modern styling
- proper spacing
- interactive states
"""
    

vision_tools = [
    generate_ui_plan
]