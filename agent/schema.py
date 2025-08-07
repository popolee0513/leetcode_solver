from typing import Optional, List, Tuple, TypedDict, Annotated
from pydantic import BaseModel, Field

class Example(BaseModel):
    input: Optional[str] = Field(default=None, description="The example input of a LeetCode problem")
    output: Optional[str] = Field(default=None, description="The expected output of a LeetCode problem")

class Information(BaseModel):
    example: List[Example] = Field(description="List of LeetCode examples")

class AgentState(TypedDict):
    examples: List[Tuple[str, str]]
    question: str
    answer: str
    QA: str