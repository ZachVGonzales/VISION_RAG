from models.ollama_models import OllamaJSONModel, OllamaModel
from termcolor import colored
from prompts import (
  router_prompt_template,
  base_promt_template
)
from state import AgentGraphState


class Agent:
  def __init__(self, state: AgentGraphState, model=None, server=None, temperature=0):
    self.state = state
    self.model = model
    self.server = server
    self.temperature = temperature

  def get_llm(self, json_model=True):
    if self.server == 'ollama':
      return OllamaJSONModel(model=self.model, temperature=self.temperature) if json_model else OllamaModel(model=self.model, temperature=self.temperature)
    
  def update_state(self, key, value):
    self.state = {**self.state, key: value}


class RouterAgent(Agent):
  def invoke(self, user_input=None, prompt=router_prompt_template):
    router_prompt = prompt

    messages = [
      {"role": "system", "content": router_prompt},
      {"role": "user", "content": f"input: {user_input}"}
    ]

    llm = self.get_llm()
    ai_msg = llm.invoke(messages)

    print(colored(f"AI message: {ai_msg}", "dark_grey"))

    response = ai_msg.content

    print(colored(f"Router 🧭: {response}", 'blue'))
    self.update_state("router_response", response)
    return self.state
  

class BaseAgent(Agent):
  def __init__(self, state, model=None, server=None, temperature=0):
    super().__init__(state, model, server, temperature)
  
  def get_llm(self, json_model=False):
    return super().get_llm(json_model=json_model)

  def invoke(self, user_input=None, prompt=base_promt_template):
    base_promt = prompt

    messages = [
      {"role": "system", "content": base_promt},
      {"role": "user", "content": f"input:{user_input}"}
    ]

    llm = self.get_llm()
    ai_msg = llm.invoke(messages)
    response = ai_msg.content

    print(colored(f"Base: {response}", 'green'))
    self.update_state("base_response", response)
    return self.state
  

class EndNodeAgent(Agent):
  def invoke(self):
    self.update_state("end_chain", "end_chain")
    return self.state

