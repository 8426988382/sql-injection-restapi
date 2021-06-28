import sqlite3


class User:

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # TODO: Improvement needed
        query = "SELECT * FROM users WHERE username='%s'" % username
        print(query)
        result = cursor.execute(query)

        result = result.fetchone()
        if result:
            user = cls(*result)
        else:
            user = None
        connection.close()

        return user

    @classmethod
    def find_by_userid(cls, userid):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # TODO: Improvement needed
        query = "SELECT * FROM users WHERE id='%s'" % userid
        print(query)
        result = cursor.execute(query)

        result = result.fetchone()
        connection.close()

        if result:
            user = cls(*result)
        else:
            user = None

        return user
