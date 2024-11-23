import os
from langchain.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import json

# 환경 변수에서 API 키 가져오기
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def load_documents_from_txt(file_path):
    """
    텍스트 파일에서 문서를 로드합니다.
    각 줄을 하나의 문서로 간주합니다.
    """
    documents = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                if line.strip():  # 빈 줄은 무시
                    documents.append(Document(page_content=line.strip()))
    except Exception as e:
        raise ValueError(f"텍스트 파일 로드 중 오류 발생: {e}")
    return documents


def create_missions(questions, weights, file_path) :


    document = load_documents_from_txt(file_path)

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectorstore = FAISS.from_documents(document, embeddings)
    retriever = vectorstore.as_retriever()

    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(
            model="gpt-4",
            temperature=0.0,
            openai_api_key=OPENAI_API_KEY
        ),
        retriever=retriever
    )


    # 질문 목록을 가중치 순으로 정렬
    sorted_questions = [q for _, q in sorted(zip(weights, questions))]

    # 가장 가중치가 낮은 질문 5개 선택
    # 5개로 했을 때가 가장 response가 좋았음
    top_5_questions = sorted_questions[:5]

    # 미션 생성을 위한 프롬프트 설정
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "당신은 유능한 미션 기획자입니다. 한국어로 주어진 항목들에 대해 명확한 구조로 미션을 만들어 주세요. "
            "결과는 반드시 JSON 형식이며, 각 미션은 'mission_name', 'description', 'duration', 'steps'로 구성됩니다. "
            "'steps'는 정확히 2개의 항목으로 배열로 구성되어야 합니다."
        ),
        (
            "human",
            "똑바로해라, 다음 항목들에 대해 가중치가 낮은 항목들에 집중하여 4개의 미션을 만들어 주세요: {questions}"
        )
    ])

    # top_5_questions를 문자열로 변환하여 프롬프트에 삽입
    questions_str = "\n".join(top_5_questions)
    missions_prompt = prompt.format(questions=questions_str)

    # OpenAI API 호출
    mission_response = qa_chain.run(missions_prompt)

    raw_content = mission_response.strip()
    if not raw_content.strip():
        raise ValueError("GPT 응답이 비어 있습니다.")
    
    # GPT 답변 파싱
    cleaned_content = raw_content.strip("```json").strip("```").strip()

    return json.loads(cleaned_content)

