import sqlite3

from flask_restful import Resource, reqparse

from models.user import UserModel
from models.card import CardModel


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
    parser.add_argument("expiry_date",
                        type=str,
                        required=True,
                        help='expiry date is missing')

    @classmethod
    def get(cls, username):

        if UserModel.find_by_username(username):
            query = "SELECT * FROM cards WHERE id in (SELECT id FROM users WHERE username='" + username + "')"

            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            cards = []
            for _id, card_type, card_number, cvv, account_holder, phone_number, expiry_date in cursor.execute(query):
                cards.append(
                    {
                        "id": _id,
                        "card_type": card_type,
                        "card_no": card_number,
                        "cvv": cvv,
                        "account_holder": account_holder,
                        "phone_number": phone_number,
                        "expiry_date": expiry_date
                    }
                )
            return {"username": username, "cards": cards}, 200

        return {'message': 'no user found'}

    @classmethod
    def post(cls, username):
        user = UserModel.find_by_username(username)
        if user:
            data = Card.parser.parse_args()

            _id = user.id
            card_type = data['card_type']
            card_no = data['card_no']
            cvv = data['cvv']
            account_holder = data['account_holder']
            phone_number = data['phone_number']
            expiry_date = data['expiry_date']

            # check if card with the provided number exists or not in the database
            print("CARD NUMBER", card_no)
            if CardModel.find_by_card_number(card_no):
                return {'message': f'Card with {card_no} already exists'}

            query = "INSERT INTO cards VALUES (? ,?, ?, ?, ?, ?, ?) "
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute(query, (_id, card_type, card_no, cvv, account_holder, phone_number, expiry_date))

            connection.commit()
            connection.close()
            return {'message': 'card added'}, 201

        return {'message': 'no user found'}, 404
