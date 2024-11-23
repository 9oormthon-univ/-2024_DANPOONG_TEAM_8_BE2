
import aiomysql
from typing import Optional, Dict
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = 30331
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


async def get_mission_content_and_feedback(member_id: int, mission_id: int) -> Optional[Dict]:
    """
    member_id와 mission_id로 미션의 content와 feedback 조회
    """
    query = """
    SELECT content, feedback 
    FROM mission_records
    WHERE member_id = %s AND mission_id = %s;
    """
    try:
        # 데이터베이스 연결 시작
        print(f"Attempting to connect to the database with member_id={member_id} and mission_id={mission_id}")
        conn = await aiomysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME,
            cursorclass=aiomysql.DictCursor
        )
        print("Database connection established.")

        # 쿼리 실행
        async with conn.cursor() as cursor:
            print(f"Executing query: {query}")
            await cursor.execute(query, (member_id, mission_id))
            result = await cursor.fetchone()
            if result:
                print(f"Fetched mission content and feedback: {result}")
                return result['content'], result['feedback']
            else:
                print(f"No record found for member_id={member_id} and mission_id={mission_id}")

        # 연결 종료
        await conn.ensure_closed()  # close() 대신 ensure_closed() 사용
        print("Database connection closed.")

        return result

    except aiomysql.MySQLError as e:
        print(f"MySQL specific error occurred: {e}")
        return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

    finally:
        # 연결이 열려 있다면 종료
        if conn:
            await conn.ensure_closed()
            print("Connection closed in finally block.")
