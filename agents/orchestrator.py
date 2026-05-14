from langchain_core.messages import SystemMessage
from services.llm import llm


ROUTER_PROMPT = """
You are an intelligent routing system for an AI Dev Assistant.

Your job is to classify the user's request and decide which agent should handle it.

You must choose ONLY ONE of the following:

- coding_agent → general coding, explanation, generation, refactoring
- debug_agent → bugs, errors, stack traces, fixes
- vision_agent → images, UI screenshots, UI design, frontend interpretation

RULES:
- Return ONLY the agent name.
- No explanation.
- No extra text.
"""


def route_user_input(state):
    print("Orchestrator running !")
    messages = state["messages"]

    # last user message
    last_msg = messages[-1].content

    prompt = [
        SystemMessage(content=ROUTER_PROMPT),
        {"role": "user", "content": str(last_msg)}
    ]

    response = llm.invoke(prompt)

    route = response.content.strip()

    # safety fallback
    allowed_routes = ["coding_agent", "debug_agent", "vision_agent"]

    if route not in allowed_routes:
        route = "coding_agent"

    return {"next": route}