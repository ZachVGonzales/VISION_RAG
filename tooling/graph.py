import json
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
from typing import Literal
from agents import (
  RouterAgent,
  BaseAgent,
  ObjectiveAgent
  )
from prompts import (
  router_prompt_template,
  base_promt_template,
  objective_prompt_template
  )
from state import AgentGraphState
from tools.objective_tool import analyze_objective


def parse_route(state: AgentGraphState) -> Literal["objective_selector", "base"]:
  route = state["router_response"]

  if route:
    route = route[-1]
  else:
    route = None
  
  if isinstance(route, HumanMessage):
    route_content = route.content
  else:
    route_content = route
  
  route_data = json.loads(route_content) if route_content else None
  next_node = route_data["next_node"] if route_data else END

  if next_node == "skip":
    return "objective_analysis"
  if next_node == "objective_analysis":
    return "objective_selector"
  else:
    return "base"


def create_graph(server=None, model=None, tempature=0):
  graph = StateGraph(AgentGraphState)
  
  graph.add_node("router",
                 lambda state: RouterAgent(
                    state=state,
                    model=model,
                    server=server,
                    temperature=tempature
                  ).invoke(
                    user_input=state["input_querry"],
                    prompt=router_prompt_template
                  ))
  
  graph.add_node("objective_selector",
                 lambda state: ObjectiveAgent(
                   state=state,
                   model=model,
                   server=server,
                   temperature=tempature
                 ).invoke(
                   user_input=state["input_querry"],
                   prompt=objective_prompt_template
                 ))
  
  graph.add_node("base",
                 lambda state: BaseAgent(
                   state=state,
                   model=model,
                   server=server,
                   temperature=tempature
                 ).invoke(
                   user_input=state["input_querry"],
                   prompt=base_promt_template
                 ))
  
  graph.add_node("objective_analysis",
                 lambda state: analyze_objective(
                   state=state
                 ))
  
  graph.add_edge(START, "router")
  graph.add_edge("objective_selector", "objective_analysis")
  graph.add_edge("objective_analysis", END)
  graph.add_edge("base", END)

  graph.add_conditional_edges(
    "router",
    lambda state: parse_route(state=state)
  )

  return graph