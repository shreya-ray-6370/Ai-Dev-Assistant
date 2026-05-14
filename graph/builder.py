from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from graph.state import State

from agents.orchestrator import route_user_input

from agents.coding_agent import (
    coding_agent,
    coding_tools
)

from agents.debug_agent import (
    debug_agent,
    debug_tools
)

from agents.vision_agent import vision_agent


# =========================
# GRAPH INIT
# =========================

graph_builder = StateGraph(State)


# =========================
# MAIN NODES
# =========================

graph_builder.add_node(
    "orchestrator",
    route_user_input
)

graph_builder.add_node(
    "coding_agent",
    coding_agent
)

graph_builder.add_node(
    "debug_agent",
    debug_agent
)

graph_builder.add_node(
    "vision_agent",
    vision_agent
)


# =========================
# TOOL NODES
# =========================

graph_builder.add_node(
    "coding_tools",
    ToolNode(coding_tools)
)

graph_builder.add_node(
    "debug_tools",
    ToolNode(debug_tools)
)


# =========================
# ENTRY
# =========================

graph_builder.add_edge(
    START,
    "orchestrator"
)


# =========================
# ORCHESTRATOR ROUTING
# =========================

graph_builder.add_conditional_edges(
    "orchestrator",
    lambda state: state["next"],
    {
        "coding_agent": "coding_agent",
        "debug_agent": "debug_agent",
        "vision_agent": "vision_agent"
    }
)


# =========================
# CODING AGENT TOOL FLOW
# =========================

graph_builder.add_conditional_edges(
    "coding_agent",
    tools_condition,
    {
        "tools": "coding_tools",
        END: END
    }
)

graph_builder.add_edge(
    "coding_tools",
    "coding_agent"
)


# =========================
# DEBUG AGENT TOOL FLOW
# =========================

graph_builder.add_conditional_edges(
    "debug_agent",
    tools_condition,
    {
        "tools": "debug_tools",
        END: END
    }
)

graph_builder.add_edge(
    "debug_tools",
    "debug_agent"
)


# =========================
# VISION AGENT
# =========================

graph_builder.add_edge(
    "vision_agent",
    END
)


# =========================
# BUILD GRAPH
# =========================

graph = graph_builder.compile()


# =========================
# OPTIONAL GRAPH VISUALIZER
# =========================

def visualize_graph():
    print(graph.get_graph().draw_ascii())