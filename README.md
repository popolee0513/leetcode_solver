# 🧠 LeetCode Solver API

這是一個使用 *FastAPI + LangGraph + OpenAI GPT-4o* 的 AI 自動解題工具。具備從 LeetCode 題目描述中提取 input/output 範例、自動產生 Python 解法、產生 assert 測試碼驗證正確性，若測試失敗則會自動重新生成，整個流程由 LangGraph 控制。

---

## 📦 啟動

- 設定 OpenAI API 金鑰：  
  export OPENAI_API_KEY="sk-xxx..."  
  （或在程式中用 os.environ 設定）

- 啟動服務：  
  uvicorn main:app --reload

- 服務將運行於 http://127.0.0.1:8000。

---

## 📬 API 使用方式

- 路由：POST /generate  
- 請求格式：  
  {"question": "LeetCode 題目描述文字"}

- 回應格式：  
  {"answer": "產生的 Python 解法", "QA": "包含測資的完整測試程式碼"}

---

## 🧪 測試 API

- 使用 test_api.py 發送測試：  
  python test_api.py

---

## 📁 專案結構

leetcode_solver/  
├── agent.py           (LangGraph agent)  
├── main.py            (FastAPI app)  
├── test_api.py        (測試用 POST 請求)  
├── requirements.txt  
└── README.md  

