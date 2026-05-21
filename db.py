import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

conn_obj = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor_obj = conn_obj.cursor(dictionary=True)

# USERS TABLE
cursor_obj.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255)
)
""")

# FILES TABLE
cursor_obj.execute("""
CREATE TABLE IF NOT EXISTS files(
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    file_name VARCHAR(255),
    file_type VARCHAR(100),
    file_url TEXT,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

conn_obj.commit()