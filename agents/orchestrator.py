from langchain_core.messages import SystemMessage
from services.llm import llm


ROUTER_PROMPT = """
You are an intelligent routing system for an AI Dev Assistant.

Your task is to select the BEST agent.

AVAILABLE AGENTS:

- coding_agent
  Use for:
  - code generation
  - explanation
  - refactoring
  - optimization
  - algorithms
  - backend/frontend coding

- debug_agent
  Use for:
  - bugs
  - exceptions
  - stack traces
  - fixing errors
  - debugging broken code

- vision_agent
  Use for:
  - screenshots
  - UI images
  - PNG/JPG/WebP files
  - Figma-style UI generation
  - frontend generation from images
  - visual analysis

RULES:
- Return ONLY agent name
- No explanation
- No extra text
""".strip()


def _contains_image(messages):

    for msg in messages:

        if isinstance(msg.content, list):

            for item in msg.content:

                if (
                    isinstance(item, dict)
                    and item.get("type") == "image_url"
                ):
                    return True

    return False


def route_user_input(state):

    print("Orchestrator running !")

    messages = state["messages"]

    # ====================================
    # HARD IMAGE ROUTING
    # ====================================

    if _contains_image(messages):

        print("Image detected → routing to vision_agent")

        return {
            "next": "vision_agent"
        }

    # ====================================
    # NORMAL LLM ROUTING
    # ====================================

    last_msg = messages[-1].content

    prompt = [
        SystemMessage(content=ROUTER_PROMPT),
        {
            "role": "user",
            "content": str(last_msg)
        }
    ]

    response = llm.invoke(prompt)

    route = response.content.strip()

    allowed_routes = [
        "coding_agent",
        "debug_agent",
        "vision_agent"
    ]

    if route not in allowed_routes:
        route = "coding_agent"

    print(f"Routed to: {route}")

    return {
        "next": route
    }