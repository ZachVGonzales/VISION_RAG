from graph import create_graph


# TODO: make this in the frontend, implement CONFIG
SERVER = "ollama"
MODEL = "deepseek-r1:1.5b"

print("creating graph...")
graph = create_graph(SERVER, MODEL)
graph = graph.compile()
print("graph created.")


if __name__ == "__main__":

  verbose = True

  while True:
    query = input("Please enter your research question: ")
    if query.lower() == "exit":
      break

    dict_inputs = {"input_querry": query}

    for event in graph.stream(dict_inputs):
      if verbose:
        print("\nState Dictionary:", event)
      else:
        print("\n")