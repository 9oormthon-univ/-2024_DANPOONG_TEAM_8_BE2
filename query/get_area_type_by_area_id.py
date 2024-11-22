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



async def get_area_type_by_area_id(area_id: str) -> Optional[int]:
    print("area_ID :", area_id)
    query = "SELECT area_type FROM areas WHERE id = %s;"

    connection = None
    try:
        # MySQL에 연결
        connection = await aiomysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME
        )
        
        async with connection.cursor() as cursor:
            await cursor.execute(query, (area_id,))
            result = await cursor.fetchone()  # 첫 번째 결과 반환
            print("Area_type", result)
            
            # result[0]으로 첫 번째 컬럼 값 반환
            return result[0] if result else None

    except Exception as e:
        # 에러 로그 출력
        print(f"Database connection error: {e}")
        return None

    finally:
        # 연결 종료
        if connection:
            connection.close()