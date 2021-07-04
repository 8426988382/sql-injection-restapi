import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

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

    """
    with auth
    """

    # @classmethod
    # @jwt_required()
    # def get(cls, username):
    #
    #     if UserModel.find_by_username(username):
    #         query = "SELECT * FROM cards WHERE id in (SELECT id FROM users WHERE username='" + username + "')"
    #
    #         connection = sqlite3.connect('data.db')
    #         cursor = connection.cursor()
    #
    #         """
    #         query = "SELECT * FROM cards WHERE id in (SELECT id FROM users WHERE username=?)"
    #
    #         connection = sqlite3.connect('data.db')
    #         cursor = connection.cursor()
    #         cursor.execute(query, (username, ))
    #         """
    #
    #         cards = []
    #         for _id, card_type, card_number, cvv, account_holder, phone_number in cursor.execute(query):
    #             cards.append(
    #                 {
    #                     "id": _id,
    #                     "card_type": card_type,
    #                     "card_no": card_number,
    #                     "cvv": cvv,
    #                     "account_holder": account_holder,
    #                     "phone_number": phone_number,
    #                 }
    #             )
    #         return {"username": username, "cards": cards}, 200
    #
    #     return {'message': 'no user found'}

    # @classmethod
    # @jwt_required()
    # def post(cls, username):
    #     user = UserModel.find_by_username(username)
    #     if user:
    #         data = Card.parser.parse_args()
    #
    #         _id = user.id
    #         card_type = data['card_type']
    #         card_no = data['card_no']
    #         cvv = data['cvv']
    #         account_holder = data['account_holder']
    #         phone_number = data['phone_number']
    #
    #         # check if card with the provided number exists or not in the database
    #         print("CARD NUMBER", card_no)
    #         if CardModel.find_by_card_number(card_no):
    #             return {'message': f'Card with {card_no} already exists'}
    #
    #         # TODO: improvement needed
    #         query = "INSERT INTO cards VALUES (?,?, ?, ?, ?, ?) "
    #         connection = sqlite3.connect('data.db')
    #         cursor = connection.cursor()
    #         cursor.execute(query, (_id, card_type, card_no, cvv, account_holder, phone_number))
    #
    #         connection.commit()
    #         connection.close()
    #         return {'message': 'card added'}, 201
    #
    #     return {'message': 'no user found'}, 404

    """
    without using auth
    """

    @classmethod
    def get(cls, username):

        if UserModel.find_by_username(username):
            query = "SELECT * FROM cards WHERE id in (SELECT id FROM users WHERE username='" + username + "')"

            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            """
            query = "SELECT * FROM cards WHERE id in (SELECT id FROM users WHERE username=?)"

            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute(query, (username, ))
            """

            cards = []
            for _id, card_type, card_number, cvv, account_holder, phone_number in cursor.execute(query):
                cards.append(
                    {
                        "id": _id,
                        "card_type": card_type,
                        "card_no": card_number,
                        "cvv": cvv,
                        "account_holder": account_holder,
                        "phone_number": phone_number,
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

            # check if card with the provided number exists or not in the database
            print("CARD NUMBER", card_no)
            if CardModel.find_by_card_number(card_no):
                return {'message': f'Card with {card_no} already exists'}

            # TODO: improvement needed
            query = "INSERT INTO cards VALUES (?,?, ?, ?, ?, ?) "
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute(query, (_id, card_type, card_no, cvv, account_holder, phone_number))

            connection.commit()
            connection.close()
            return {'message': 'card added'}, 201

        return {'message': 'no user found'}, 404
