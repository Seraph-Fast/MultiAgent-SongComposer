# logging.py
import psycopg2
from psycopg2 import sql
from datetime import date, time, timedelta

# Database connection setup (replace with your actual credentials)
DB_PARAMS = {
    'dbname': 'poet_db',
    'user': 'composer_user',
    'password': '1234',
    'host': 'localhost',
    'port': 5432
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
