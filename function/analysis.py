import os
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import re

load_dotenv()
# 환경 변수에서 API 키 가져오기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


AREA_QUESTIONS = {
    1: "DAILY_LIFE",
    2: "SELF_MANAGEMENT"
}

def get_questions_by_area(area_type):

    """area_id에 따라 질문 카테고리 반환"""
    if area_type == 'DAILY_LIFE':
        return [
            "영양성분을 고려한 주간 식단표를 계획할 수 있다.",
            "식품을 구매할 때 제조일자와 유통기한을 확인한다.",
            "조리법에 따라서 음식을 조리할 수 있고 사람 수에 따라 음식 양을 조절할 수 있다.",
            "어떤 음식이 냉장보관 또는 냉동보관이 필요한지 알고 있고, 음식이 상했는지 구별할 수 있다.",
            "식사준비 시에 적절하게 주방기구를 사용하고, 사용한 후 주방기구를 깨끗하게 정리정돈 할 수 있다.",
            "집안청소(화장실, 침실, 가스레인지 등)를 할 수 있고, 방 정리정돈(책상, 서랍, 옷장 등)상태를 유지할 수 있다.",
            "적절한 쓰레기 처리 방법(재활용, 음식물 등)을 알고 있다.",
            "의류라벨 지시에 따른 세탁방법, 세탁기 사용법, 옷 건조, 건조대와 다리미 사용을 포함한 의복관리방법을 알고 있다."
        ]
    elif area_type == 'MONEY_MANAGEMENT':
        return [
            "한 달 동안 쓰는 돈의 수입과 지출을 파악할 수 있다.",
            "용돈기입장을 사용하고 있다.",
            "공과금에 대하여 알고 있다.",
            "휴대폰을 쓸 경우 요금을 내야하는 책임이 있으며, 요금을 연체했을 경우 받는 불이익에 대해 알고 있다.",
            "본인의 통장을 개설할 수 있다.",
            "인터넷 뱅킹을 사용할 수 있다.",
            "자립을 위한 저축액(디딤씨앗통장, 후원금, 용돈 등)을 매월 확인하고 있다.",
            "19세부터 건강보험 납부의무가 있다는 것을 알고 있다."
        ]
    elif area_type == 'SELF_MANAGEMENT':
        return [
            "건강을 위한 생활습관이 잘 되어있다.(예를 들어, 규칙적인 생활, 예방주사, 손 씻기, 양치질하기, 치과검진 등)",
            "성(性)적 행동을 결정하기 전에 반드시 고려해야할 사항이 무엇인지 알고 있다.",
            "성폭력 피해 시 도움을 받을 수 있는 긴급전화 등 한 가지 이상의 방법을 알고 있다.",
            "성적접촉으로 인해 생길 수 있는 위험(에이즈, 매독, 임질 등)을 알고 있고 예방법을 이해하고 있다.",
            "담배, 술, 약물 등을 누군가 권유했을 때 거절할 수 있다.",
            "바람직한 이성교제에 대하여 알고 있다.",
            "응급상황이 발생했을 때 상황에 따른 응급처치 요령을 알고 있다.",
            "건강상태, 가족의 질병경험, 병원기록 등을 묻는 질문에 대답할 수 있다."

        ]
    elif area_type == 'SOCIETY':
        return [
            "나의 생각이나 감정을 다른 사람에게 명확하게 표현할 수 있다.",
            "화를 내지 않고 나에 대한 충고를 들을 수 있다.",
            "대인관계를 맺는데 어려움이 없다.",
            "다른 사람과 갈등이 있을 때 대처할 수 있는 방법이 있다.",
            "필요할 때 남에게 도움을 요청할 수 있다.",
            "타인의 요청을 기분 상하지 않게 거절할 수 있다.",
            "지역 도서관, 운동모임, 기타동호회 등에 속해 있다.",
            "내가 위험에 처했을 때 나를 도와줄 수 있는 사람이 있다."
        ]

def generate_analysis_response(db_result, area_type):


    print("분석에서 받아오는 : \n",db_result)
    print("분석에서 받아오는 AREA_TYPE : \n", area_type)
    try:
        general_llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        results = []
        
        entry = db_result[0]
        print("entry입니다!", entry)
        user_id = entry['id']
        area_id = entry['area']
        member = entry['member']
        answers = entry['questions']

        questions = get_questions_by_area(area_type)
        
        answer_texts = ['매우 못한다', '못한다', '잘한다', '매우 잘한다']
        mapped_answers = []
        
        for idx, question in enumerate(questions):
            key = f'{["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth"][idx]}Q'
            answer_value = answers.get(key, 0)
            answer_text = answer_texts[answer_value - 1] if 1 <= answer_value <= 4 else '답변 없음'
            
            mapped_answers.append(f"{question} => {answer_text}")
        print("mapped_answers", mapped_answers)
        analysis_input = "\n".join(mapped_answers)

        prompt = f"""
                사용자가 다음 질문에 답변했습니다:
                {analysis_input}

                결과는 반드시 JSON 형식으로만 제공되어야 하며, JSON 객체에는 content 키만 포함되어야 합니다. 
                사용자에 대한 종합 분석을 수행하고, 사용자의 8가지 질문에 대한 응답을 간단하게!! 분석해주세요. 
                잘하는 부분은 칭찬하고, 개선이 필요한 부분도 설명해주세요.
                """

        response = general_llm(prompt)
        
        
        results.append({
            "user_id": user_id,
            "area_id": area_id,
            "area_type" : area_type,
            "member": member,
            "analysis": {"content": response}
        })
    
        return {"report": results}
    
    except Exception as e:
        print(f"예상치 못한 오류 발생: {e}")
        return {"report": []}
    

