from fastapi import FastAPI, HTTPException, Header, Query
from pydantic import BaseModel
from query.get_character_type_by_id import get_character_type_by_user
from function.chat_bot import custom_chatbot
from query.get_userid_by_kakao import get_userID
from function.create_missions import create_missions
app = FastAPI()


# 요청 모델 정의
class QuestionRequest(BaseModel):
    question: str

# 테스트 데이터
questions = [
    "영양가 있는 식단을 계획하는 방법?",
    "청소할 때 필요한 필수 도구는 무엇인가요?",
    "효과적인 공부 시간 관리 방법?",
    "옷을 깨끗하게 관리하는 법?",
    "쓰레기 분리수거 규칙은?",
    "건강한 식단의 예시?",
    "효율적인 장보기 요령은?"
]
weights = [3, 2, 5, 4, 1, 6, 2]



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


@app.get("/generate-missions/", tags=["AI_mission_generate & Custom_analysis"], 
        description="Kakao ID를 기반으로 사용자 맞춤형 분석을 진행하고 미션을 DB에 저장하는 API입니다.", 
        )
async def generate_missions(
    kakao_id: str = Header(..., description= "카카오 사용자 ID"),
    
):
    """
    Kakao ID를 헤더에서 받아, 사용자 맞춤형 미션을 생성합니다.
    """
    # Kakao ID를 이용해 member_id 조회
    member_id = await get_userID(kakao_id)

    if not member_id:
        raise HTTPException(status_code=404, detail="해당 Kakao ID에 대한 사용자 정보를 찾을 수 없습니다.")

    all_missions = create_missions(questions, weights)
    print("ALL_MISSIONS: ",all_missions)
    
    return {"result": all_missions}

