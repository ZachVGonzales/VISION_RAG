from fastapi import FastAPI, HTTPException
from transformers import pipeline

"""
run with: uvicron main:app --host 0.0.0.0 --port 8084
"""

app = FastAPI()

# TODO: insert model path or config
# load the objective classifier model 
classifier = pipeline("text-classification", model="need to insert model path here or path to config")

@app.post
async def predict(text: str):
  try:
    results = classifier(text)
    return {"results": results}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))