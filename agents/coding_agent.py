from langchain_core.messages import SystemMessage

from services.llm import llm, vision_llm
from tools.file_tools import read_uploaded_file
from prompts.coding_prompt import CODING_PROMPT


coding_tools = [
    read_uploaded_file
]

llm_with_tools = llm.bind_tools(coding_tools)


def _has_image(messages):

    for msg in messages:

        if isinstance(msg.content, list):

            for part in msg.content:

                if (
                    isinstance(part, dict)
                    and part.get("type") == "image_url"
                ):
                    return True

    return False


def coding_agent(state):

    recent_messages = state["messages"][-10:]

    selected_file = state.get("selected_file")

    system_prompt = CODING_PROMPT

    if selected_file:

        system_prompt += f"""

CURRENT SELECTED FILE:
{selected_file}

IMPORTANT:
- Always use this selected file when reading code.
- Do not ask user again for filename.
"""

    messages = [
        SystemMessage(content=system_prompt),
        *recent_messages
    ]

    if _has_image(recent_messages):
        response = vision_llm.invoke(messages)
    else:
        response = llm_with_tools.invoke(messages)

    return {"messages": [response]}