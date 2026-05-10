from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from state import State
from agent import coding_assistant
from tools.file_tools import tools


graph_builder = StateGraph(State)


graph_builder.add_node(
    "coding_assistant",
    coding_assistant
)

graph_builder.add_node(
    "tools",
    ToolNode(tools)
)


graph_builder.add_edge(
    START,
    "coding_assistant"
)

graph_builder.add_conditional_edges(
    "coding_assistant",
    tools_condition,
    {
        "tools": "tools",
        END: END
    }
)

graph_builder.add_edge(
    "tools",
    "coding_assistant"
)


graph = graph_builder.compile()