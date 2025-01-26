from graph import create_graph
from IPython.display import Image


if __name__ == "__main__":
  graph = create_graph("ollama", "deepseek-r1:1.5b")
  graph = graph.compile()
  png_data = graph.get_graph().draw_mermaid_png()
  with open("graph_pic/graph_image.png", "wb") as file:
    file.write(png_data)

  