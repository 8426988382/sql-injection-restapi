import sqlite3

from db import db


class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # TODO: Improvement needed
        query = "SELECT * FROM (SELECT * FROM users WHERE username='%s'" % username + ")"
        result = cursor.execute(query)

        """
        query = "SELECT * FROM users WHERE username=?'
        result = cursor.execute(query, (username, ))
        """

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
        result = cursor.execute(query)

        """
        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (userid, ))
        """

        result = result.fetchone()
        connection.close()

        if result:
            user = cls(*result)
        else:
            user = None

        return user
