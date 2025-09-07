# 4-stream_ages.py

import sqlite3

def stream_user_ages():
    """
    Generator that yields user ages one by one
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row[0]
    conn.close()

def calculate_average_age():
    """
    Calculate the average age using the generator
    without loading all data into memory
    """
    total = 0
    count = 0
    for age in stream_user_ages():  # loop 1
        total = total + age   # explicit "+" required
        count = count + 1
    if count > 0:
        average_age = total / count  # division for average
        print(f"Average age of users: {average_age}")
    else:
        print("No users found.")

if __name__ == "__main__":
    calculate_average_age()
