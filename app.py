import sqlite3

from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity


app = Flask(__name__)
app.secret_key = '1234addfdg'
api = Api(app)


jwt = JWT(app, authenticate, identity)  # /auth


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
        print("USERNAME: ", username, " PASSWORD: ", password)

        query = 'INSERT INTO users VALUES (NULL, ?, ?)'

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        cursor.execute(query, (username, password))
        connection.commit()
        connection.close()

        return {'message': 'user created'}, 201


api.add_resource(UserRegister, '/user/register')

if __name__ == '__main__':
    app.run(debug=True)

