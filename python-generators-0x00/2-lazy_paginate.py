# 2-lazy_paginate.py

import sqlite3

def paginate_users(page_size, offset):
    """
    Fetch one page of users starting from given offset.
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data LIMIT ? OFFSET ?", (page_size, offset))
    rows = cursor.fetchall()
    conn.close()
    return rows

def lazy_paginate(page_size):
    """
    Generator that yields pages of users lazily.
    """
    offset = 0
    while True:  # only one loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size


if __name__ == "__main__":
    # Example run
    for page in lazy_paginate(2):
        print(page)

