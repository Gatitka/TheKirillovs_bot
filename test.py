import sqlite3

try:
    conn = sqlite3.connect('accountant.db')
    cursor = conn.cursor()

    # cursor.execute("INSERT INTO 'users' ('user_id') VALUES (?)", (1000,))
    users = cursor.execute("SELECT * FROM 'users'")
    print(users.fetchall())
    conn.commit()

except sqlite3.Error as error:
    print("Error", error)

finally:
    if (conn):
        conn.close()
