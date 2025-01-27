enum Node {
  OBJECTIVE_ANALYSIS
  BASE
}


class ObjectiveAnalysis {
  objective string @description(#"
    an objective such as "the student shall jump."
  "#)
}

class QuestionAnswering {
  querry string @description(#"
    a question such as "why is the sky blue?"
  "#)
}


class Route {
  node Node
}


class Objective {
  objective string
}


function ChooseNextNode(user_message: string) -> Route {
  client DeepSeekR1
  prompt #"
    You are a router. Your task is to route the conversation to the next node of action based on the input provided by the user.
You must choose one of the following nodes: OBJECTIVE_ANALYSIS, BASE.

### Criteria for Choosing the Next Node:
- **OBJECTIVE_ANALYSIS**: If objective analysis is requested by the user.
- **BASE**: Any other use case than the one's listed previously.

user input:
    ---
    {{user_message}}
    ---

    {{ctx.output_format(prefix="you must provide your response in the following json format:")}}
  "#
}


function DetectObjective(user_message: string) -> Objective {
  client DeepSeekR1
  prompt #"
    Your task is to detect the objective in the provided input text.

input text:
    ---
    {{user_message}}
    ---

    {{ctx.output_format(prefix="you must provide your response in the following json format:")}}
  "#
}


function ChooseTool(user_message: string) -> ObjectiveAnalysis | QuestionAnswering {
  client DeepSeekR1
  prompt #"
    Choose the right schema that contains all the information in this message:
    ---
    {{user_message}}
    ---

    {{ctx.output_format}}

    JSON:
  "#
}