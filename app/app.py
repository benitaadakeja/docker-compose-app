from flask import Flask
import mysql.connector
import os
import time

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host="database",
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

def initialize_database():
    while True:
        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS visits (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            connection.commit()
            cursor.close()
            connection.close()
            break

        except mysql.connector.Error:
            time.sleep(2)

@app.route("/")
def home():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("INSERT INTO visits () VALUES ()")
    connection.commit()

    cursor.execute("SELECT COUNT(*) FROM visits")
    count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return f"""
    <h1>Hello from Docker Compose!</h1>
    <p>This page has been visited <strong>{count}</strong> times.</p>
    """

if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=5000)
