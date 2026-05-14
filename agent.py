# from langchain_core.messages import SystemMessage

# from services.llm import llm, vision_llm
# from tools.file_tools import tools
# from prompts.coding_prompt import CODING_PROMPT

# llm_with_tools = llm.bind_tools(tools)


# def _has_image(messages):
#     for msg in messages:
#         if isinstance(msg.content, list):
#             for part in msg.content:
#                 if isinstance(part, dict) and part.get("type") == "image_url":
#                     return True
#     return False


# def coding_assistant(state):

#     recent_messages = state["messages"][-10:]
#     clean_messages = recent_messages
#     messages = [SystemMessage(content=CODING_PROMPT)] + clean_messages

#     if _has_image(recent_messages):
#         response = vision_llm.invoke(messages)
#     else:
#         response = llm_with_tools.invoke(messages)

#     return {"messages": [response]}