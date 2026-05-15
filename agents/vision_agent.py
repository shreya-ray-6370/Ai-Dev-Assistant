from langchain_core.messages import SystemMessage

from services.llm import vision_llm

from prompts.vision_prompt import VISION_PROMPT


def vision_agent(state):

    print("Vision Agent running !")

    recent_messages = state["messages"][-10:]

    selected_file = state.get("selected_file")

    system_prompt = VISION_PROMPT

    if selected_file:

        system_prompt += f"""

CURRENT IMAGE FILE:
{selected_file}

IMPORTANT:
- Analyze this uploaded image carefully
- Generate frontend code matching the image
- Maintain layout accuracy
- Maintain responsiveness
"""

    messages = [
        SystemMessage(content=system_prompt),
        *recent_messages
    ]

    response = vision_llm.invoke(messages)

    return {
        "messages": [response]
    }