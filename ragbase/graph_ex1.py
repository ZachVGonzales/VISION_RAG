from typing import TypedDict
from typing import Literal
import random
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
  graph_state = str


"""
Node's take in the graph state alter it in 
some way and then return the new graph state
"""
def node_1(state: State):
  print("---Node 1---")
  return {"graph_state": state['graph_state'] + "I am"}

def node_2(state: State):
  print("---Node 2---")
  return {"graph_state": state['graph_state'] + "happy"}

def node_3(state: State):
  print("---Node 3---")
  return {"graph_state": state['graph_state'] + "sad"}


"""
Edges connect the Nodes,
Normal edges are used if you want to go from node 1 to node 2 directly.
Conditional edges are used to optionally route between nodes.
Conditional edges implimented as a function that returns the next node 
based on some logic
"""
def decide_mood(state: State) -> Literal["node_2", "node_3"]:
  # simple case so next state is decided randomly
  if random.random() < 0.5:
    return "node_2"
  return "node_3"


def main():
  
  # build graph:
  builder = StateGraph(State)
  builder.add_node("node_1", node_1)
  builder.add_node("node_2", node_2)
  builder.add_node("node_3", node_3)

  # graph logic
  builder.add_edge(START, "node_1")
  builder.add_conditional_edges("node_1", decide_mood)
  builder.add_edge("node_2", END)
  builder.add_edge("node_3", END)

  # compile
  graph = builder.compile()

  graph.invoke({"graph_state": ""})


if __name__ == "__main__":
  main()