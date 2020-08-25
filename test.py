import sqlite3

with sqlite3.connect("data.db") as connection:
    cursor = connection.cursor()
    
    create_table = "CREATE TABLE users (id int, username text, password text)"
    cursor.execute(create_table)
    
    user = (1, 'jose', 'asdf')
    insert_query = "INSERT INTO users VALUES (?,?,?)"
    cursor.execute(insert_query, user)
    
    users = [
        (2, 'aami', 'qwer'),
        (3, 'ameer', 'zxcv')
    ]
    
    cursor.executemany(insert_query, users)
    
    select_query = "SELECT * FROM users"
    for row in cursor.execute(select_query):
        print(row)
    
    connection.commit()
