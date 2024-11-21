import aiomysql
from typing import Optional
from dotenv import load_dotenv
from get_userid_by_kakao import get_userID
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = 30331
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")



async def get_character_type_by_user(kakao_id: str) -> Optional[str]:
    """
    주어진 kakao_id에 매핑된 사용자 ID로 character 테이블에서 해당 사용자의 character_type을 조회.

    Args:
        kakao_id (str): 조회할 카카오 ID.

    Returns:
        str: 카카오 ID에 매핑된 사용자 ID의 character_type. 없으면 None 반환.
    """
    try:
        # 먼저 사용자의 ID를 가져옴
        user_id = await get_userID(kakao_id)
        
        if not user_id:
            print(f"User ID not found for kakao_id: {kakao_id}")
            return None
        
        # 사용자 ID로 character 테이블에서 character_type 조회
        query = "SELECT character_type FROM characters WHERE member_id = %s;"
        
        # MySQL에 연결
        connection = await aiomysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME
        )

        async with connection.cursor() as cursor:
            await cursor.execute(query, (user_id,))
            result = await cursor.fetchone()  # 첫 번째 결과 반환
            
            if result:
                return result[0]  # 첫 번째 컬럼(character_type)을 반환
            return None  # 결과가 없을 경우 None 반환

    except Exception as e:
        # 에러 로그 출력
        print(f"Database connection error: {e}")
        return None

    finally:
        # 연결 종료
        if connection:
            await connection.ensure_closed()
