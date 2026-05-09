from llm import llm


def coding_assistant(state):

    response = llm.invoke(state["messages"])

    return {
        "messages": [response]
    }