import os
import sqlite3


home = os.environ['HOME']
db_path = f'{home}/Code/forge/py_forge/termgpt/memory/chat_memory.db'


def init_db(path=db_path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL CHECK(role IN ('user', 'assistant', 'system')),
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    return conn


def main():
    init_db()


if __name__ == "__main__":
    main()
