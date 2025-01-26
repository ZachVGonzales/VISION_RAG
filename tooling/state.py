
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

# Define the state object for the agent graph
class AgentGraphState(TypedDict):
  input_querry: str
  objective_analysis_response: Annotated[list, add_messages]
  router_response: Annotated[list, add_messages]
  base_response: Annotated[list, add_messages]
  end_chain: Annotated[list, add_messages]
    
state = {
    "input_querry": "",
    "objective_analysis_response": [],
    "router_response": [],
    "base_response": [],
    "end_chain": []
}
