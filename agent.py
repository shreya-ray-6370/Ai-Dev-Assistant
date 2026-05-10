from llm import llm
from tools.file_tools import tools


llm_with_tools = llm.bind_tools(tools)


def coding_assistant(state):
    response = llm_with_tools.invoke(state["messages"])

    return {
        "messages": [response]
    }