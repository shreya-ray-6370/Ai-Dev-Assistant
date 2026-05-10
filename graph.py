from langgraph.graph import StateGraph, START, END

from state import State
from agent import coding_assistant


graph_builder = StateGraph(State)


graph_builder.add_node(
    "coding_assistant",
    coding_assistant
)


graph_builder.add_edge(
    START,
    "coding_assistant"
)

graph_builder.add_edge(
    "coding_assistant",
    END
)


graph = graph_builder.compile()