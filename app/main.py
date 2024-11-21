from fastapi import FastAPI, HTTPException, Header, Query
from pydantic import BaseModel
from query.get_character_type_by_id import get_character_type_by_user
from function.chat_bot import custom_chatbot


app = FastAPI()


# 요청 모델 정의
class QuestionRequest(BaseModel):
    question: str

@app.post("/api/ask", tags=['AI_ask'], description="사용자와 소통할 수 있는 맞춤형 감성 챗봇입니다. 선택한 캐릭터에 따라 대답하는 아이가 달라집니다.")
async def ask_question(request: QuestionRequest, kakao_id: str = Header(...)):
    try:
        # 카카오 ID로 character_type 조회
        character_type = await get_character_type_by_user(kakao_id)
         # 함수 호출 시 character_type 전달

        if not character_type:
            raise HTTPException(status_code=404, detail="Character type not found for the user.")
        
       
        print("request입니다" , request)
        print("캐릭터타입니다", character_type)
        answer = custom_chatbot(request.question, character_type)
        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

