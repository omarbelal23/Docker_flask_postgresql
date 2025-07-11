from flask import Flask
import psycopg2
import os

app = Flask(__name__)

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
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT version();')
    db_version = cur.fetchone()
    cur.close()
    conn.close()
    return f'متصل بـ PostgreSQL بنجاح 🚀<br>النسخة: {db_version[0]}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'أهلا بيك في أول مشروع Docker مع Flask! 🚀'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

