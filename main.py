from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Tuple
import os
import openai

# ✅ 設定 API 金鑰
os.environ['OPENAI_API_KEY'] = openai.api_key = ""

# ✅ 匯入 Agent 類別
from agent.agent import Agent

app = FastAPI()
abot = Agent()

class QuestionRequest(BaseModel):
    question: str

class AgentResult(BaseModel):
    answer: str
    

@app.post("/generate")
async def generate(request: QuestionRequest):
    try:
        question = request.question
        # 你的 Agent 調用程式碼
        result = abot.graph.invoke({"question": question})
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}