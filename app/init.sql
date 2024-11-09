-- init.sql

CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    date DATE,
    start_time TIME,
    end_time TIME,
    query_time INTERVAL,
    user_proxy_response TEXT,
    data_assistant_response TEXT,
    original_poet_response TEXT,
    composer_response TEXT
);
