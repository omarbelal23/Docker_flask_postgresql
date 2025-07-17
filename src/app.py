from flask import Flask
import psycopg2
import redis
import os

app = Flask(__name__)

# Redis connection
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_client = redis.Redis(host=redis_host, port=6379, decode_responses=True)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("POSTGRES_DB"),
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD")
    )
    return conn

@app.route('/')
def home():
    # Check Redis cache first
    db_version = redis_client.get("db_version")

    if db_version:
        source = "📦 Redis Cache"
    else:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT version();')
        db_version = cur.fetchone()[0]
        cur.close()
        conn.close()
        # Save in Redis with 60-second expiry
        redis_client.setex("db_version", 60, db_version)
        source = "🐘 PostgreSQL"

    return f'ﺖﺼﻠﺘﺑ ﺐـ {source} ﺐﻨﺟﺎﺣ 🚀<br>ﺎﻠﻨﺴﺧﺓ: {db_version}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

