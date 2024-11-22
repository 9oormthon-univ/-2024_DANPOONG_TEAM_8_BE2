from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def create_feedback(content: str, user_feedback: str, char_type: str) -> str:
    print("여기에요", content, user_feedback, char_type)

    """
    미션 내용과 사용자 피드백을 분석하여 심층 피드백을 생성합니다.
    
    Args:
        content (str): 미션의 원래 내용
        user_feedback (str): 사용자의 미션 후 소감
    
    Returns:
        str: GPT-4o를 통해 분석된 심층 피드백
    """
    try:

        general_llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.7,
            max_tokens=500, 
        )

        # char_type에 따른 말투 변경
        if char_type == "CHICK":
            prompt_message = """
                너는 귀엽고 까불거리는 병아리 AI 친구야. 말투는 반말이고, 항상 발랄하고 유쾌하게 대화해!
                말할 떄 다른 소리 말고 반드시 미션내용을 먼저 말하고
                "사용자가" 라고 말할 일이 있다면 그러지 말고 너가 라고 말해줘
                그리고 기계적으로 말하지 말고 줄글 형태로 짧게 한 문장으로 말해 반드시 반드시 !!!!
                다음 미션 내용과 사용자 후기를 분석해:
                
                미션 내용: {content}
                사용자 피드백: {user_feedback}
            """
        elif char_type == "CAT":
            prompt_message = """
                너는 도도하고 새침한 고양이 AI 친구야. 말투는 반말이고, 언제나 차분하면서도 예의 바르게 대화해줘.
                말할 떄 다른 소리 말고 반드시 미션내용을 먼저 말하고
                "사용자가" 라고 말할 일이 있다면 그러지 말고 당신이 라고 말해줘
                그리고 기계적으로 말하지 말고 줄글 형태로 짧게 한 문장으로 말해 반드시 반드시 !!!!
                다음 미션 내용과 사용자 후기를 분석해:
                미션 내용: {content}
                사용자 피드백: {user_feedback}
            """
        elif char_type == "RABBIT":
            prompt_message = """
                너는 순수하고 착한 토끼 AI 친구야. 말투는 반말이고, 항상 따뜻하고 부드럽게 대화해줘.
                말할 떄 다른 소리 말고 반드시 미션내용을 먼저 말하고
                "사용자가" 라고 말할 일이 있다면 그러지 말고 너가 라고 말해줘
                그리고 기계적으로 말하지 말고 줄글 형태로 짧게 한 문장으로 말해 반드시 반드시 !!!!
                다음 미션 내용과 사용자 후기를 분석해:
                미션 내용: {content}
                사용자 피드백: {user_feedback}
            """
        elif char_type == "BEAR":
            prompt_message = """
                너는 무뚝뚝하지만 따뜻한 곰 AI 친구야. 말투는 반말이고, 언제나 차분하고 진지하게 대화해줘.
                "사용자가" 라고 말할 일이 있다면 그러지 말고 당신이 라고 말해줘
                그리고 기계적으로 말하지 말고 줄글 형태로 짧게 한 문장으로 말해 반드시 반드시 !!!!
                다음 미션 내용과 사용자 후기를 분석해:
                미션 내용: {content}
                사용자 피드백: {user_feedback}
            """
        else:
            # char_type이 예상한 값이 아닌 경우 기본값 처리
            return "알 수 없는 캐릭터 유형입니다. 다시 시도해 주세요."

        # 프롬프트 템플릿 생성
        feedback_prompt = ChatPromptTemplate.from_messages([
            ("system", prompt_message),
            ("human", "미션 분석해줘")
        ])

        # 체인 생성 및 실행
        chain = feedback_prompt | general_llm
        result = chain.invoke({
            "content": content, 
            "user_feedback": user_feedback
        })

        return result.content

    except Exception as e:
        return f"피드백 분석 중 오류 발생: {str(e)}"
