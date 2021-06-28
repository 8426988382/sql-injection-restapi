import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# user table
create_user_table = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)'
cursor.execute(create_user_table)

create_card_table = "CREATE TABLE IF NOT EXISTS cards (id int, card_no int, cvv int, account_holder text, " \
                    "phone_number text, email text) "
cursor.execute(create_card_table)

print("CARDS")
for row in cursor.execute('SELECT * FROM cards'):
    print(row)


print("USERS")
cursor1 = connection.cursor()
for user in cursor1.execute('SELECT * FROM users'):
    print(user)



connection.commit()
connection.close()


# users => id (primary key), username, password
# cards => id, card number, ...
