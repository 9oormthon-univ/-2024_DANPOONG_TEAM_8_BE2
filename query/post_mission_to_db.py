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



# 데이터베이스에 미션 삽입 함수
async def insert_mission_to_db(mission_data):
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
        conn = await aiomysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME
        )
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

                for i in range(2) :
                    await cursor.execute(steps_query, (steps[i]))
        
        await conn.commit()
        conn.close()
        print("미션 삽입 완료")
        return {"success": True, "message": "Missions inserted successfully"}
    
    except Exception as e:
        error_message = f"Error inserting mission: {str(e)}"
        print(error_message)
        return {"error": error_message}
