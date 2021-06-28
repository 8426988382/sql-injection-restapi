import sqlite3

connection = sqlite3.connect('data.db')

create_table = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)'
cursor = connection.cursor()
cursor.execute(create_table)

for row in cursor.execute('SELECT * FROM users'):
    print(row)


connection.commit()
connection.close()


