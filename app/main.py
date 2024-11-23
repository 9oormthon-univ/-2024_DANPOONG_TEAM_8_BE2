from fastapi import FastAPI, HTTPException, Header, Query
from pydantic import BaseModel
from query.get_character_type_by_id import get_character_type_by_user, get_character_info
from function.chat_bot import custom_chatbot
from query.get_userid_by_kakao import get_userID
from function.create_missions import create_missions
from fastapi.middleware.cors import CORSMiddleware  # CORS 미들웨어 import
from function.buddy_comment import create_feedback
from query.get_mission_content import get_mission_content_and_feedback
from query.get_check_lists_by_id import fetch_check_lists


app = FastAPI()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 오리진 허용, 필요시 특정 도메인으로 제한 가능
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)


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
    "집 가기! "
]
weights = [3, 2, 5, 4, 1, 6, 2, 7]


@app.post("/api/ask", tags=['AI_ask'], description="사용자와 소통할 수 있는 맞춤형 감성 챗봇입니다. 선택한 캐릭터에 따라 대답하는 아이가 라집니다.")
async def ask_question(request: QuestionRequest, kakao_id: str = Header(...)):
    try:
        # 카카오 ID로 character_type 조회
        character_type = await get_character_type_by_user(kakao_id)
         # 함수 호출 시 character_type 전달

        if not character_type:
            raise HTTPException(status_code=404, detail="Character type not found for the user.")
        
        print("request입니다" , request)
        print("캐릭터타입니다", character_type)
        answer = custom_chatbot(request.question, character_type[0])
        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/generate-missions/", tags=["AI_mission_generate & Custom_analysis"], 
        description="Kakao ID를 기반으로 사용자 맞춤형 분석을 진행하고 미션을 DB에 저장하는 API입니다.", 
        )
async def generate_missions(
    kakao_id: str = Header(..., description= "카카오 사용자 ID"),
    check_list_id: int = Query(..., description= "사용자 설문 ID"),

):
    """
    Kakao ID를 헤더에서 받아 사용자 맞춤형 미션을 생성합니다.
    """
    # Kakao ID를 이용해 member_id 조회
    member_id = await get_userID(kakao_id)

    
    if not member_id:
        raise HTTPException(status_code=404, detail="해당 Kakao ID에 대한 사용자 정보를 찾을 수 없습니다.")
    
    # 사용자 ID 기반 데이터베이스 조회
    print("체크리스트 아이디 :", check_list_id)

    db_result = await fetch_check_lists(check_list_id)
    print("DB_RESULT\n", db_result)
    print("DB_AREA\n", db_result[0]['area'])
    all_missions = create_missions(questions, weights)

    print("ALL_MISSIONS: ",all_missions)
    
    return {"result": all_missions}


@app.post("/api/buddy-feedback", tags=['Buddy_Feedback'], 
          description="사용자가 미션에 대한 버디 피드백을 제공하는 API입니다.")
async def provide_buddy_feedback(
    kakao_id: str = Header(..., description="카카오 사용자 ID", alias="kakao-id"),  # Header의 경우 하이픈 사용
    mission_id: int = Query(..., description="피드백을 제공할 미션의 ID"),  # mission_id는 1 이상의 정수
):
    try:
        # 나머지 코드는 동일
        member_id = await get_userID(kakao_id)
        print(member_id)
        print(mission_id)
        if not member_id:
            raise HTTPException(status_code=404, detail="Kakao ID not found.")
            
        level, char_type = await get_character_info(member_id)
        print(level, char_type, "레벨과 캐릭터타입 \n")
        content, feedback = await get_mission_content_and_feedback(member_id, mission_id)
        
        feedback_result = create_feedback(content, feedback, char_type)
        
        return {
            "status": "success",
            "message": "Feedback submitted successfully.",
            "buddy_feedback": feedback_result,
            "char_type": char_type,
            "character_level": level,
            "user_mission" : content,
            "user_feedback" : feedback
        }

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        print(f"Error in provide_buddy_feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))