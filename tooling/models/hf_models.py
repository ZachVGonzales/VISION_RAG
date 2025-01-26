import requests
import json
from langchain_core.messages.human import HumanMessage


class ObjectiveClassifierModel:
  def __init__(self, temperature=0):
    self.headers = {"Content-Type": "application/json"}
    self.model_endpoint = "http://localhost:8084/predict"
    self.temperature = temperature

  def invoke(self, objective):

    payload = {
      "text": objective
    }
        
    try:
      request_response = requests.post(
        self.model_endpoint, 
        headers=self.headers, 
        data=json.dumps(payload)
      )
        
      print("REQUEST RESPONSE", request_response)
      request_response_json = request_response.json()
      # print("REQUEST RESPONSE JSON", request_response_json)
      response = json.loads(request_response_json['response'])
      response = json.dumps(response)

      response_formatted = HumanMessage(content=response)

      return response_formatted
    except requests.RequestException as e:
      response = {"error": f"Error in invoking model! {str(e)}"}
      response_formatted = HumanMessage(content=response)
      return response_formatted
