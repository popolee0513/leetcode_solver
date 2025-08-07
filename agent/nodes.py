from .schema import Information
from langchain.utils.openai_functions import convert_pydantic_to_openai_function
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

def extract_example(state):
    question = state['question']
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    extraction_functions = [convert_pydantic_to_openai_function(Information)]
    extraction_model = model.bind(
        functions=extraction_functions,
        function_call={"name": "Information"}
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Think carefully, and then tag the text as instructed"),
        ("user", "{input}")
    ])

    tagging_chain = prompt | extraction_model | JsonOutputFunctionsParser()

    examples = []
    parsed = tagging_chain.invoke({"input": question})['example']
    for item in parsed:
        examples.append((item['input'], item['output']))

    return {'examples': examples}

def generate_python_code(state):
    question = state['question']
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    system_message = """
    You are a senior software engineer who is an expert in Python, data structures, and algorithms.
    Your job is to write clean, correct, and executable Python code that solves the given LeetCode-style problem.
    Do not explain the code. Do not add comments or markdown formatting. Just return the raw Python code that works.
    """

    code_prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", "{question}"),
    ])

    code_solver = code_prompt | llm | StrOutputParser()
    answer = code_solver.invoke({"question": question})
    return {'answer': answer}

def run_tests(state):
    test_code = state["QA"]
    try:
        exec(test_code, {})
        return "Correct"
    except Exception:
        return "Incorrect"

def generate_tests(state):
    python_code = state['answer']
    examples = state['examples']

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    system_message = """
    You are a QA expert specializing in checking Python code correctness.
    Given a piece of Python code and a list of example input-output pairs, 
    generate test code that verifies whether the given code produces the expected outputs.

    Requirements:
    - Do NOT redefine the function.
    - Do NOT use print statements.
    - Use assert statements to validate outputs.
    - Return ONLY executable Python test code.
    - Do NOT include any explanation or markdown formatting.
    """

    human_message = f"""
    Here is the Python code to test:

    {python_code}

    Here are example input-output pairs for testing:

    {examples}

    Please generate the testing Python code as instructed.
    """

    code_prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", human_message),
    ])

    code_tester = code_prompt | llm | StrOutputParser()
    test_code_only = code_tester.invoke({}).replace("```python", "").replace("```", "").strip()
    full_test_code = f"{python_code}\n\n{test_code_only}"
    return {'QA': full_test_code}