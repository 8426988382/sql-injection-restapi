import sqlite3

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# major function is ORM

connection = sqlite3.connect('data.db')
for row in connection.cursor().execute('SELECT * FROM cards'):
    print(row)
