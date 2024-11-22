import aiomysql
from typing import List, Dict, Optional
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = 30331
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


# 데이터베이스에서 check_lists 테이블 조회 함수 (user_id 기반)
async def fetch_check_lists(check_list_id):
    query = """
        SELECT id, fistQ, secondQ, thirdQ, fourthQ, fifthQ, sixthQ, seventhQ, eighthQ, area_id, member_id
        FROM check_lists
        WHERE id = %s;
    """
    try:
        # DB 연결
        conn = await aiomysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME,
            cursorclass=aiomysql.DictCursor
        )
        
        async with conn.cursor() as cursor:
            await cursor.execute(query, (check_list_id,))
            result = await cursor.fetchall()

        # 연결 종료
        conn.close()
        
        # 결과 처리 (check_lists 데이터를 mission_data 형식으로 가공)
        mission_data = []
        for row in result:
            # 각 항목에서 필요한 데이터를 mission 데이터로 변환
            mission_item = {
                "id": row.get("id"),
                "questions": {
                    "firstQ": row.get("fistQ"),
                    "secondQ": row.get("secondQ"),
                    "thirdQ": row.get("thirdQ"),
                    "fourthQ": row.get("fourthQ"),
                    "fifthQ": row.get("fifthQ"),
                    "sixthQ": row.get("sixthQ"),
                    "seventhQ": row.get("seventhQ"),
                    "eighthQ": row.get("eighthQ")
                },
                "area": row.get("area_id"),
                "member": row.get("member_id")
            }
            mission_data.append(mission_item)

        return mission_data
    except Exception as e:
        print(f"Error fetching check_lists: {str(e)}")
        return {"error": str(e)}
