import sqlite3

import flask
from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='username required')

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='password required')

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        username = data['username']
        password = data['password']

        if UserModel.find_by_username(username):
            return {"message": "username is in use"}

        query = 'INSERT INTO users VALUES (NULL, ?, ?)'

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        cursor.execute(query, (username, password))
        connection.commit()
        connection.close()

        return {'message': 'user_created'}, 201
