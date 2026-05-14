from typing import Annotated, Optional
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages


class State(TypedDict):

    # conversation history
    messages: Annotated[list, add_messages]

    # uploaded files available
    uploaded_files: list[str]

    # currently selected file
    selected_file: Optional[str]

    # classified task type
    task_type: Optional[str]

    # active agent
    active_agent: Optional[str]

    # image presence
    contains_image: bool

    # final response
    final_response: Optional[str]