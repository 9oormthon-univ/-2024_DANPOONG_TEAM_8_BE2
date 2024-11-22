import aiomysql
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()


DB_HOST = os.getenv("DB_HOST")
DB_PORT = 30331
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Function to execute a query
async def execute_query(query: str, params=None):
    """
    Executes a query on the MariaDB database.
    :param query: SQL query string.
    :param params: Tuple of parameters for the query (optional).
    """
    try:
        # Connect to MariaDB with DictCursor
        conn = await aiomysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME,
            cursorclass=aiomysql.DictCursor
        )
        async with conn.cursor() as cursor:
            # Execute query with parameters
            await cursor.execute(query, params)
            
            # Fetch SELECT results
            if query.strip().lower().startswith("select"):
                result = await cursor.fetchall()
            else:
                await conn.commit()  # Commit for INSERT, UPDATE, DELETE
                result = "Query executed successfully"
        
        # Close connection
        conn.close()
        return result
    except Exception as e:
        return {"error": str(e)}

# Example usage
async def main():
    # Example INSERT query for all fields
    insert_query = """
        INSERT INTO missions (
            mission_name, is_completed, member_id, area_id,
            description, duration
        ) 
        VALUES (%s, %s, %s, %s, %s, %s);
    """
    # Example data

    
    params = (
    
        "Sample Mission",  # missionName
        0,  # isCompleted
        1,  # member
        1,  # area
        "This is a sample mission for testing.",  # description
        "2h",  # duration
    )
    result = await execute_query(insert_query, params)
    print(result)

# Run the event loop
asyncio.run(main())
