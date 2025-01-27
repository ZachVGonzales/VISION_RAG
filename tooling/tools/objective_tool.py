import json
from state import AgentGraphState
from langchain_core.messages import HumanMessage
from termcolor import colored

def analyze_objective(state: AgentGraphState):
  # TODO: implement call to objective analysis tool here:
  response = state["obj_selector_response"][-1]
  print(colored(f"response: {response}, {type(response)}", "red"))
  response_data = json.loads(response.content)
  print(response_data)
  objective = response_data["objective"]
  print(objective)

  analysis = f"would analyze objective: {objective}"

  state["objective_analysis_response"].append(HumanMessage(role="system", content=analysis))
  return state