# 1-batch_processing.py

import sqlite3

def stream_users_in_batches(batch_size):
    """
    Yield rows from user_data table in batches
    """
    conn = sqlite3.connect("users.db")  # assumes users.db exists
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

def batch_processing(batch_size):
    """
    Process each batch and yield users over the age of 25
    """
    for batch in stream_users_in_batches(batch_size):
        yield [user for user in batch if user[2] > 25]  # user[2] = age


if __name__ == "__main__":
    # Example run: prints filtered batches
    for filtered_batch in batch_processing(3):
        print(filtered_batch)

