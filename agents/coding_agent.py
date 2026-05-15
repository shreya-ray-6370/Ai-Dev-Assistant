from langchain_core.messages import SystemMessage

from services.llm import llm

from prompts.coding_prompt import CODING_PROMPT

from tools.coding_tools import coding_tools


llm_with_tools = llm.bind_tools(coding_tools)


def coding_agent(state):

    print("Coding Agent running !")

    recent_messages = state["messages"][-10:]

    selected_file = state.get("selected_file")

    system_prompt = CODING_PROMPT

    if selected_file:

        system_prompt += f"""

CURRENT SELECTED FILE:
{selected_file}

IMPORTANT:
- Always use this selected file
- Do not ask for filename again
"""

    messages = [
        SystemMessage(content=system_prompt),
        *recent_messages
    ]

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }