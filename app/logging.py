# logging.py
import psycopg2
from psycopg2 import sql
from datetime import date, time, timedelta
from typing import List, Dict
from app.config import DBSettings


settings = DBSettings()

# Database connection setup (replace with your actual credentials)
DB_PARAMS = {
    'dbname': settings.POSTGRES_DB,
    'user': settings.POSTGRES_USER,
    'password': settings.POSTGRES_PASSWORD,
    'host': settings.POSTGRES_HOST,
    'port': settings.POSTGRES_PORT
}

def log_interaction(date: date, start_time: time, end_time: time, query_time: timedelta,
                    user_proxy_response: str, data_assistant_response: str,
                    original_poet_response: str, composer_response: str):
    """
    Logs the interaction details into the PostgreSQL database using psycopg2.
    
    Args:
    - date (date): The date of the query.
    - start_time (time): The time the query started.
    - end_time (time): The time the query ended.
    - query_time (timedelta): The duration of the query.
    - user_proxy_response (str): Response from the user proxy.
    - data_assistant_response (str): Response from data assistant.
    - original_poet_response (str): Response from the original poet agent.
    - composer_response (str): Response from the composer agent.
    """
    
    # Establish a connection
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()

    # Insert log into the database
    insert_query = sql.SQL("""
        INSERT INTO logs (date, start_time, end_time, query_time, user_proxy_response, 
                          data_assistant_response, original_poet_response, composer_response)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """)
    
    cursor.execute(insert_query, (
        date,
        start_time,
        end_time,
        query_time,
        user_proxy_response,
        data_assistant_response,
        original_poet_response,
        composer_response
    ))
    
    # Commit and close connection
    conn.commit()
    cursor.close()
    conn.close()

def get_logs() -> List[Dict]:
    try:
        # Connect to the database
        connection = psycopg2.connect(**DB_PARAMS)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM logs ORDER BY date DESC")
        logs = cursor.fetchall()

        log_data = [
            {
                "log_id": log[0],
                "date": log[1],
                "start_time": log[2],
                "end_time": log[3],
                "query_time": log[4],
                "user_proxy_response": log[5],
                "data_assistant_response": log[6],
                "original_poet_response": log[7],
                "composer_response": log[8]
            }
            for log in logs
        ]

        # Close the connection
        cursor.close()
        connection.close()

        return log_data
    except Exception as e:
        print(f"Error fetching logs: {e}")
        return []