from langchain_core.messages import SystemMessage

from services.llm import llm
from tools.file_tools import read_uploaded_file
from prompts.debug_prompt import DEBUG_PROMPT


debug_tools = [
    read_uploaded_file
]

llm_with_tools = llm.bind_tools(debug_tools)


def debug_agent(state):

    recent_messages = state["messages"][-10:]

    selected_file = state.get("selected_file")

    system_prompt = DEBUG_PROMPT

    if selected_file:

        system_prompt += f"""

CURRENT SELECTED FILE:
{selected_file}

IMPORTANT:
- Always use this selected file.
- Use it for debugging tasks.
- Do not ask user for filename again.
"""

    messages = [
        SystemMessage(content=system_prompt),
        *recent_messages
    ]

    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}