from fastapi import FastAPI, HTTPException, Header, Query
from pydantic import BaseModel

app = FastAPI()


# 요청 모델 정의
class QuestionRequest(BaseModel):
    question: str

@app.post("/api/ask", tags=['AI_ask'], description="사용자와 소통할 수 있는 맞춤형 감성 챗봇입니다. 선택한 캐릭터에 따라 대답하는 아이가 달라집니다.")
async def ask_question(request: QuestionRequest):
    try:
        return {"answer": request}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

