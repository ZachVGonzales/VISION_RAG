from langchain.agents import initialize_agent, Tool, AgentType
from langchain_huggingface.llms import HuggingFacePipeline
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

# Set up the Hugging Face model (you can replace with a different model if needed)
MODEL_NAME = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"  # Example model; you can use any Hugging Face model

# Define a simple tool for arithmetic calculations
def calculate_expression(expression: str) -> str:
  try:
    result = eval(expression)
    return str(result)
  except Exception as e:
    return f"Error: {str(e)}"

# Run the chatbot
if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

    # Create the Hugging Face pipeline with max_new_tokens set
    hf_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=100)
    hf_pipeline = HuggingFacePipeline(pipeline=hf_pipeline)

    # Create a list of tools for the agent
    tools = [ 
        Tool(
            name="Calculator",
            func=calculate_expression,
            description="Can evaluate mathematical expressions."
        ),
    ]

    # Initialize the agent with the tools and LLM (HuggingFacePipeline)
    agent = initialize_agent(
        tools, hf_pipeline, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )
    
    # Start the chatbot
    while True:
      user_input = input("You: ")
      if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

      # Pass user input to the agent
      response = agent.invoke([user_input])
      print(f"Bot: {response}")