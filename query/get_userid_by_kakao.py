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


async def get_userID(kakao_id: str) -> Optional[int]:
    """
    주어진 kakao_id에 매핑된 id를 member 테이블에서 조회.

    Args:
        kakao_id (str): 조회할 카카오 ID.

    Returns:
        int: kakao_id에 매핑된 사용자 ID. 없으면 None 반환.
    """
    query = "SELECT id FROM member WHERE kakao_id = %s;"

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
            await cursor.execute(query, (kakao_id,))
            result = await cursor.fetchone()  # 첫 번째 결과 반환
            
            if result:
                return result[0]  # 첫 번째 컬럼(ID)을 반환
            return None  # 결과가 없을 경우 None 반환

    except Exception as e:
        # 에러 로그 출력
        print(f"Database connection error: {e}")
        return None

    finally:
        # 연결 종료
        if connection:
            await connection.ensure_closed()
        
