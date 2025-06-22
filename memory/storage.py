import sqlite3

def save_message(conn: sqlite3.Connection, role: str, content: str):
    """
    Save a chat message to the database.
    role: 'user', 'assistant', or 'system'
    content: message text
    """
    conn.execute(
        "INSERT INTO chat_memory (role, content) VALUES (?, ?)",
        (role, content)
    )
    conn.commit()


def load_recent_messages(conn: sqlite3.Connection, limit: int = 10):
    """
    Load recent chat messages ordered oldest to newest.
    Returns a list of dicts with 'role' and 'content'.
    """
    cursor = conn.execute(
        "SELECT role, content FROM chat_memory ORDER BY timestamp DESC LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()
    # Reverse so oldest first
    return [{"role": row[0], "content": row[1]} for row in reversed(rows)]
