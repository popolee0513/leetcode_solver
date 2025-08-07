from langgraph.graph import StateGraph, END
from .schema import AgentState
from .nodes import extract_example, generate_python_code, generate_tests, run_tests

class Agent:
    def __init__(self):
        graph = StateGraph(AgentState)
        graph.add_node("extract", extract_example)
        graph.add_node("python_expert", generate_python_code)
        graph.add_node("QA expert", generate_tests)
        graph.add_edge("extract", "python_expert")
        graph.add_edge("python_expert", "QA expert")
        graph.add_conditional_edges("QA expert", run_tests, {
            "Correct": END,
            "Incorrect": "python_expert"
        })

        graph.set_entry_point("extract")
        self.graph = graph.compile()