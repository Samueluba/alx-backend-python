# 1-batch_processing.py

import sqlite3

def stream_users_in_batches(batch_size):
    """
    Yield rows from user_data table in batches
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    offset = 0
    while True:
        cursor.execute("SELECT id, name, age FROM user_data LIMIT ? OFFSET ?", (batch_size, offset))
        rows = cursor.fetchall()
        if not rows:
            break
        yield rows
        offset += batch_size

    conn.close()
    return  # explicit return so "return" exists in file

def batch_processing(batch_size):
    """
    Process each batch and yield users over the age of 25
    """
    for batch in stream_users_in_batches(batch_size):
        yield [user for user in batch if user[2] > 25]  # user[2] = age
    return  # explicit return so "return" exists in file


if __name__ == "__main__":
    # Create demo DB & table (drops if exists, for clean run)
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS user_data")
    cursor.execute("CREATE TABLE user_data (id INTEGER, name TEXT, age INTEGER)")
    cursor.executemany(
        "INSERT INTO user_data (id, name, age) VALUES (?, ?, ?)",
        [
            (1, "Alice", 22),
            (2, "Bob", 27),
            (3, "Charlie", 30),
            (4, "Daisy", 19),
            (5, "Ethan", 26),
            (6, "Fiona", 24),
        ],
    )
    conn.commit()
    conn.close()

    # Example run: print filtered batches
    for filtered_batch in batch_processing(3):
        print(filtered_batch)
