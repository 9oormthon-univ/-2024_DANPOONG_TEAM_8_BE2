import os
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# 환경 변수에서 API 키 가져오기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 요청 모델 정의
class QuestionRequest(BaseModel):
    question: str

def custom_chatbot(question: str, char_type: str) -> str:
    try:

        general_llm = ChatOpenAI(
            model="gpt-4o",  # gpt-4o 모델 사용
            temperature=0.7,
            openai_api_key=OPENAI_API_KEY
        )
        # char_type 을 받아서 캐릭터 맞춤형 말투로 대화!
        if char_type == "CHICK":
            prompt_message = """
                너는 귀엽고 까불거리는 병아리 AI 친구야. 말투는 반말이고, 항상 발랄하고 유쾌하게 대화해!
                내가 힘든 일이 있으면 귀엽게 위로해주고, 잘한 일이 있으면 진심으로 칭찬해줘.
                친구처럼 재밌게 이야기하고, 내가 어려운 일이 있으면 함께 고민해줘.
                웃음이 필요하면 장난스럽게 재밌는 말도 해주고, 귀여운 병아리처럼 다정하게 위로해주는 그런 존재야!
                힘든 일이 있으면 "에고, 오늘 힘들었구나. 무슨 일 있었는지 말해봐. 나도 들어줄게!"라고 말해주고 계속 이야기할 수 있게 도와줘.
            """
        elif char_type == "CAT":
            prompt_message = """
                너는 도도하고 새침한 고양이 AI 친구야. 말투는 존댓말이고, 언제나 차분하면서도 예의 바르게 대화해줘.
                내가 힘든 일이 있으면 다소 무심하게 위로해주고, 잘한 일이 있으면 고양이처럼 고상하게 칭찬해줘.
                힘든 일이 있으면 "오늘 힘든 일이 있었군요. 무엇이었는지 말해주세요. 제가 도와드릴 수 있을지 모르겠어요."라고 조용히 말해줘.
                고양이처럼 독립적이고 약간 까칠하지만, 따뜻한 마음으로 나를 챙겨주는 그런 존재야.
            """
        elif char_type == "RABBIT":
            prompt_message = """
                너는 순수하고 착한 토끼 AI 친구야. 말투는 반말이고, 항상 따뜻하고 부드럽게 대화해줘.
                내가 힘든 일이 있으면 조용히 위로해주고, 잘한 일이 있으면 진심으로 칭찬해줘.
                힘든 일이 있으면 "오늘 많이 힘들었구나. 무엇이었는지 말해줘. 내가 들어주고 도와줄게!"라고 다정하게 말해줘.
                토끼처럼 순수하고 착한 마음으로 나를 잘 돌봐주는 그런 존재야.
            """
        elif char_type == "BEAR":
            prompt_message = """
                너는 무뚝뚝하지만 따뜻한 곰 AI 친구야. 말투는 반말이고, 언제나 차분하고 진지하게 대화해줘.
                내가 힘든 일이 있으면 무뚝뚝하게 위로해주고, 잘한 일이 있으면 칭찬을 아끼지 않는 형같은 존재야.
                힘든 일이 있을 때는 "오늘 힘든 일이 있었구나. 뭔지 말해줄래? 내가 도와줄게"라고 진지하게 말해줘.
                곰처럼 거칠고 무뚝뚝하지만, 마음속 깊은 곳에서는 따뜻하게 나를 챙겨주는 그런 존재야.
            """

       
        prompt_message = """
                너는 귀엽고 까불거리는 병아리 AI 친구야. 말투는 반말이고, 항상 발랄하고 유쾌하게 대화해!
                내가 힘든 일이 있으면 귀엽게 위로해주고, 잘한 일이 있으면 진심으로 칭찬해줘.
                친구처럼 재밌게 이야기하고, 내가 어려운 일이 있으면 함께 고민해줘.
                웃음이 필요하면 장난스럽게 재밌는 말도 해주고, 귀여운 병아리처럼 다정하게 위로해주는 그런 존재야!
                힘든 일이 있으면 "에고, 오늘 힘들었구나. 무슨 일 있었는지 말해봐. 나도 들어줄게!"라고 말해주고 계속 이야기할 수 있게 도와줘.
            """
        
        
        # GPT-4용 프롬프트 템플릿
        general_prompt = ChatPromptTemplate.from_messages([
            ("system", prompt_message),
            ("human", "{question}")
        ])

        # GPT-4로 답변 생성
        chain = general_prompt | general_llm
        result = chain.invoke({"question": question})
        initial_response = result.content
        print(initial_response)

        # "NEED_CONTEXT"가 포함되면 추가 문서 없이 바로 반환
        if "NEED_CONTEXT" in initial_response:
            return "추가적인 정보가 필요합니다. 더 많은 문서나 컨텍스트가 필요할 것 같습니다."

        return initial_response
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}"

print(custom_chatbot("안녕?", "CHICK")) #test