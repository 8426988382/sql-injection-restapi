import sqlite3

from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from user import User

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

        if User.find_by_username(username):
            return {"message": "username is in user"}

        query = 'INSERT INTO users VALUES (NULL, ?, ?)'

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        cursor.execute(query, (username, password))
        connection.commit()
        connection.close()

        return {'message': 'user created'}, 201


class Card(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("card_type",
                        type=str,
                        required=True,
                        help='card_number is missing')
    parser.add_argument("card_no",
                        type=int,
                        required=True,
                        help='card_number is missing')
    parser.add_argument("cvv",
                        type=int,
                        required=True,
                        help='cvv is missing')
    parser.add_argument("account_holder",
                        type=str,
                        required=True,
                        help='id is missing')
    parser.add_argument("phone_number",
                        type=str,
                        required=True,
                        help='id is missing')

    @classmethod
    @jwt_required()
    def get(cls, username):
        query = "SELECT * FROM cards WHERE id in (SELECT id FROM users WHERE username='" + username + "')"
        print(query)

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        cards = []
        for _id, card_number, cvv, account_holder, phone_number, email in cursor.execute(query):
            cards.append(
                {
                    "id": _id,
                    "card_no": card_number,
                    "cvv": cvv,
                    "account_holder": account_holder,
                    "phone_number": phone_number,
                    "email": email
                }
            )
        return {"username": username, "cards": cards}, 200

    @classmethod
    @jwt_required()
    def post(cls, username):
        user = User.find_by_username(username)
        if user:
            data = Card.parser.parse_args()

            _id = user.id
            card_type = data['card_type']
            card_no = data['card_no']
            cvv = data['cvv']
            account_holder = data['account_holder']
            phone_number = data['phone_number']

            # TODO: improvement needed
            query = "INSERT INTO cards VALUES (?,?, ?, ?, ?, ?) "
            print("POST CARD QUERY ", query)
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute(query, (_id, card_type, card_no, cvv, account_holder, phone_number))

            connection.commit()
            connection.close()
            return {'message': 'card added'}, 201

        return {'message': 'no user found'}, 404


api.add_resource(UserRegister, '/user/register')
api.add_resource(Card, '/card/<string:username>')

if __name__ == '__main__':
    app.run(debug=True)
