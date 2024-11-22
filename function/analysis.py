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
    if area_type == '1' :
        print(1)
    elif area_type == '2' :
        print(2)

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
