from state import AgentGraphState
from langchain_core.messages import HumanMessage


def analyze_objective(state: AgentGraphState):
  # TODO: implement call to objective analysis tool here:
  analysis = "objective analyzer called: output would appear here..."

  state["objective_analysis_response"].append(HumanMessage(role="system", content=analysis))
  return {"objective_analysis_response": state["objective_analysis_response"]}