from dotenv import load_dotenv
import os
from unittest.mock import MagicMock

load_dotenv()

# 환경변수 불러오기
DB_HOST = os.getenv("DB_HOST")
DB_PORT = 30331
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# 데이터베이스에 미션 삽입 함수
async def insert_mission_to_db(mission_data, conn):
    print("받은 mission_data :", mission_data)
    
    query = """
        INSERT INTO missions (
            is_completed, area_id, member_id, 
            description, duration, mission_name
        ) 
        VALUES (%s, %s, %s, %s, %s, %s);
    """
    steps_query = """
        INSERT INTO mission_steps (mission_id, steps) 
        VALUES (LAST_INSERT_ID(), %s);
    """
    
    try:
        print(f"DB 연결 성공: {DB_HOST}:{DB_PORT} - {DB_NAME}")
       
        area_id = mission_data["area_id"]
        member_id = mission_data["member"]
        missions_list = mission_data["missions_list"]
            
        if not area_id or not member_id:
            print(f"Skipping mission due to missing area_id or member_id: {mission_data}")
            return {"error": "Missing area_id or member_id"}
            
        for mission_item in missions_list:
            mission_name = mission_item["mission_name"]
            description = mission_item["description"]
            duration = mission_item["duration"]
            steps = mission_item["steps"]
            
            # 미션 데이터 삽입
            params = (0, area_id, member_id, description, duration, mission_name)
            print(f"Inserting mission: {params}")
            async with conn.cursor() as cursor:
                await cursor.execute(query, params)

                for step in steps:
                    await cursor.execute(steps_query, (step,))
        
        await conn.commit()
        print("미션 삽입 완료")
        return {"success": True, "message": "Missions inserted successfully"}
    
    except Exception as e:
        error_message = f"Error inserting mission: {str(e)}"
        print(error_message)
        return {"error": error_message}


# 미션 데이터 예시 (Multiple Missions)
mission_data_2 = {
    "area_id": 2,
    "member": 456,
    "missions_list": [
        {
            "mission_name": "코드 리뷰",
            "description": "팀원들의 코드 리뷰를 하고 피드백을 제공하기",
            "duration": 2,
            "steps": ["코드 분석", "피드백 작성", "리뷰 회의 진행"]
        },
        {
            "mission_name": "프로젝트 발표 준비",
            "description": "프로젝트 발표를 위한 자료 준비 및 발표 리허설 진행",
            "duration": 3,
            "steps": ["슬라이드 준비", "발표 연습", "발표 리허설"]
        }
    ]
}


# 테스트용 데이터베이스 모킹(mocking)
async def test_insert_mission():
    # 예시 데이터 중 하나를 선택해서 테스트
    mission_data = mission_data_2  # 다양한 미션 데이터 중 하나를 사용 가능

    # 데이터베이스 연결을 모킹(mocking)하려면 mock_conn을 사용
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__aenter__.return_value = mock_cursor
    mock_cursor.execute.return_value = None  # 쿼리 실행이 정상적으로 완료된 것처럼 설정
    
    # insert_mission_to_db 함수 실행
    result = await insert_mission_to_db(mission_data, mock_conn)
    print(result)


# 실제 테스트 실행
import asyncio
asyncio.run(test_insert_mission())
